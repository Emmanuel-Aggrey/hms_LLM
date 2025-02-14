from django.db import models
from accounts.models import User
from django.utils import timezone
from core.models import BaseModel
from doctorsnote.models import DoctorsNote


class ActionableTask(BaseModel):

    class TASK_TYPE:
        CHECKLIST = "checklist"
        PLAN = "plan"

        CHOICES = (
            (CHECKLIST, ("One-time Task")),
            (PLAN, ("Scheduled Task")),
        )

        ALL = [CHECKLIST, PLAN]

    class STATUS:
        PENDING = "pending"
        COMPLETED = "completed"
        CANCELLED = "cancelled"

        CHOICES = (
            (PENDING, ("Pending")),
            (COMPLETED, ("Completed")),
            (CANCELLED, ("Cancelled")),
        )

        ALL = [PENDING, COMPLETED, CANCELLED]

    class REMINDER_STATUS:
        SCHEDULED = "scheduled"
        SENT = "sent"
        ACKNOWLEDGED = "acknowledged"

        CHOICES = (
            (SCHEDULED, ("Scheduled")),
            (SENT, ("Sent")),
            (ACKNOWLEDGED, ("Acknowledged")),
        )

        ALL = [SCHEDULED, SENT, ACKNOWLEDGED]

    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='patient_tasks')
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='doctor_tasks')
    task_type = models.CharField(max_length=10, choices=TASK_TYPE.CHOICES)
    description = models.TextField()
    status = models.CharField(
        max_length=10, choices=STATUS.CHOICES, default=STATUS.PENDING)
    reminder_status = models.CharField(
        max_length=15,
        choices=REMINDER_STATUS.CHOICES,
        default=REMINDER_STATUS.SCHEDULED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    repeat_count = models.IntegerField(default=1)
    current_repetition = models.IntegerField(default=0)
    note = models.ForeignKey(DoctorsNote, on_delete=models.CASCADE)
    last_reminder_sent = models.DateTimeField(null=True, blank=True)
    next_reminder_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['scheduled_date', 'created_at']

    def mark_completed(self):
        self.status = self.STATUS.COMPLETED
        self.completion_date = timezone.now()
        self.reminder_status = self.REMINDER_STATUS.ACKNOWLEDGED
        self.save()

    def should_reschedule(self):
        return (
            self.task_type == self.TASK_TYPE.PLAN and
            self.current_repetition < self.repeat_count and
            self.status != self.STATUS.CANCELLED
        )
