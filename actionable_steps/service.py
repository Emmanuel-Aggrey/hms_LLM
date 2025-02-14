from rest_framework.exceptions import ValidationError
import json
import logging
from typing import Dict, List
from requests.models import Response
from actionable_steps.models import ActionableTask
from datetime import timedelta
from django.utils import timezone
from actionable_steps.tasks import schedule_reminder
logger = logging.getLogger(__name__)


class ActionableStepsService:
    def __init__(self):
        self.required_sections = [
            f'{ActionableTask.TASK_TYPE.CHECKLIST}:', f'{ActionableTask.TASK_TYPE.PLAN}:']

    def extract_actionable_steps(self, doctor_notes: str) -> Dict[str, List[str]]:

        if not isinstance(doctor_notes, str) or not doctor_notes.strip():
            raise ValidationError(detail={
                                  "detail": "Doctor notes must be a non-empty string"}, code="invalid_request")

        prompt = self._create_prompt(doctor_notes)

        try:
            from core.dependency_injection import service_locator
            response = service_locator.core_service.generate_response(prompt)
            response_text = self._extract_response_text(response)
            actionable_steps = self.parse_response(response_text)

            if not any(actionable_steps.values()):
                logger.warning("No actionable steps extracted from notes")

            return actionable_steps

        except Exception as e:
            logger.error(f"Failed to process doctor notes: {str(e)}")
            raise ValidationError(
                detail={
                    "detail": f"Failed to process doctor notes: {str(e)}",
                },
                code="invalid_request"
            )

    def _create_prompt(self, doctor_notes: str) -> str:
        return f"""
        Extract actionable steps from the following doctor's notes and categorize them into:
        1. checklist: Immediate one-time tasks (e.g., purchase medication, schedule test)
        2. plan: Scheduled actions with specific timelines (e.g., take medication daily for 7 days)

        Format all tasks as clear, actionable instructions.
        Doctor's Notes: "{doctor_notes}"

        Output Format:
        checklist:
        - [Task 1]
        - [Task 2]

        plan:
        - [Action 1 with timeline]
        - [Action 2 with timeline]
        """

    def _extract_response_text(self, response: Response) -> str:
        if response.status_code != 200:
            logger.error(
                f"LLM API error: {response.status_code} - {response.text}")
            raise ValidationError(
                detail={
                    "detail": f"LLM API request failed with status code {response.status_code}",
                },
                code="invalid_request"
            )

        try:
            response_json = response.json()
            generated_text = response_json["candidates"][0]["content"]["parts"][0]["text"]

            if not all(section in generated_text for section in self.required_sections):
                raise ValidationError(detail={
                    "detail": "LLM response missing required sections",
                }, code="invalid_response")

            return generated_text

        except (KeyError, IndexError, json.JSONDecodeError) as e:
            logger.error(f"Failed to parse LLM response: {str(e)}")
            raise ValidationError(detail={
                "detail": f"Failed to parse LLM response: {str(e)}",
            }, code="invalid_response")

    def parse_response(self, response_text: str) -> Dict[str, List[str]]:

        result = {
            ActionableTask.TASK_TYPE.CHECKLIST: [],
            ActionableTask.TASK_TYPE.PLAN: []
        }
        current_section = None

        for line in response_text.split("\n"):
            line = line.strip()
            if not line:
                continue

            if "checklist:" in line:
                current_section = ActionableTask.TASK_TYPE.CHECKLIST
            elif "plan:" in line:
                current_section = ActionableTask.TASK_TYPE.PLAN
            elif line.startswith("- ") and current_section:
                task = line[2:].strip()
                task = task.replace("[", "").replace("]", "").strip()

                if task:  # Only add non-empty tasks
                    result[current_section].append(task)

        return result

    # SchedulingService

    def create_tasks_from_llm_output(self, llm_output, patient, doctor, note_id):
        # Cancel existing tasks for this patient
        ActionableTask.objects.filter(
            patient=patient,
            status=ActionableTask.STATUS.PENDING
        ).update(status=ActionableTask.STATUS.CANCELLED)

        tasks_created = []

        # Create checklist (one-time) tasks
        for task in llm_output.get(ActionableTask.TASK_TYPE.CHECKLIST, []):
            scheduled_date = timezone.now()
            task_obj = ActionableTask.objects.create(
                patient=patient,
                doctor=doctor,
                task_type=ActionableTask.TASK_TYPE.CHECKLIST,
                description=task,
                scheduled_date=scheduled_date,
                next_reminder_date=scheduled_date,
                note_id=note_id
            )
            # Schedule immediate reminder for checklist task
            schedule_reminder.delay(task_obj.id)
            tasks_created.append(task_obj)

        # Create plan (scheduled) tasks
        for task in llm_output.get(ActionableTask.TASK_TYPE.PLAN, []):
            duration, frequency = self._parse_plan_task(task)
            scheduled_date = timezone.now()

            task_obj = ActionableTask.objects.create(
                patient=patient,
                doctor=doctor,
                task_type=ActionableTask.TASK_TYPE.PLAN,
                description=task,
                scheduled_date=scheduled_date,
                next_reminder_date=scheduled_date,
                repeat_count=duration,
                note_id=note_id
            )
            # Schedule first reminder for plan task
            schedule_reminder.delay(task_obj.id)
            tasks_created.append(task_obj)

        return tasks_created

    def _parse_plan_task(self, task_description):
        """
        Parses a plan task to extract duration and frequency
        Example: "take medication daily for 7 days" -> (7, 1)
        """
        words = task_description.lower().split()
        duration = 1
        frequency = 1

        try:
            if 'days' in words:
                idx = words.index('days') - 1
                duration = int(words[idx])
            elif 'weeks' in words:
                idx = words.index('weeks') - 1
                duration = int(words[idx]) * 7
        except (ValueError, IndexError):
            pass

        return duration, frequency

    def process_task_completion(self, task_id, patient_id):
        """Processes task completion and handles rescheduling if needed"""
        try:
            task = ActionableTask.objects.get(
                id=task_id,
                patient_id=patient_id,
                status=ActionableTask.STATUS.PENDING
            )
        except ActionableTask.DoesNotExist:
            raise ValidationError(detail={
                "detail": "Task not found or none pending",
            }, code="task_not_found")

        task.current_repetition += 1

        if task.should_reschedule():
            new_scheduled_date = task.scheduled_date + timedelta(days=1)
            task.scheduled_date = new_scheduled_date
            task.next_reminder_date = new_scheduled_date
            task.reminder_status = ActionableTask.REMINDER_STATUS.SCHEDULED
            task.save()

            # Schedule next reminder
            schedule_reminder.delay(task.id)
        else:
            task.mark_completed()

        return task
