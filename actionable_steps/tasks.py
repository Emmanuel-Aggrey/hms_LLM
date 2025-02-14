from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from actionable_steps.models import ActionableTask
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def schedule_reminder(task_id):
    """Schedule a single reminder for a task"""
    try:
        task: ActionableTask = ActionableTask.objects.get(id=task_id)

        send_reminder_notification(task)

        task.last_reminder_sent = timezone.now()
        task.reminder_status = ActionableTask.REMINDER_STATUS.SENT
        task.save()

        # If task needs to be rescheduled
        if task.should_reschedule():
            next_reminder = task.scheduled_date + timedelta(days=1)
            task.next_reminder_date = next_reminder
            task.save()

            # Schedule next reminder
            schedule_reminder.apply_async(
                args=[task.id],
                eta=next_reminder
            )

    except ActionableTask.DoesNotExist:
        pass


@shared_task
def check_pending_reminders():
    """Periodic task to check and schedule pending reminders"""
    now = timezone.now()
    pending_tasks = ActionableTask.objects.filter(
        status=ActionableTask.STATUS.PENDING,
        reminder_status=ActionableTask.REMINDER_STATUS.SCHEDULED,
        scheduled_date__lte=now + timedelta(minutes=5)
    )

    for task in pending_tasks:
        schedule_reminder.delay(task.id)


def send_reminder_notification(task: ActionableTask):
    subject = f'Reminder: {task.description}'
    message = f"""
    This is a reminder for your scheduled task: {task.description}\
        Please complete this task and mark it as done in your dashboard.
    """

    # Send email
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [task.patient.email],
        fail_silently=False,
    )
