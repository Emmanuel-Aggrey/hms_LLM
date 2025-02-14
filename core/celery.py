"""
http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
"""
import os
from celery.schedules import crontab
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.base")


app = Celery("core",)

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {

    'check-pending-reminders': {
        'task': 'actionable_steps.tasks.check_pending_reminders',
        'schedule': crontab(minute='*/5'),  # Run every 5 minutes
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


@app.task(bind=True)
def test_celery(self):
    return 'Celery is working!'
