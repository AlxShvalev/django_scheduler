import os

from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'file_scheduler.settings')


app = Celery('file_scheduler')
app.config_from_object('django.conf:settings', namespace='CELERY')


@setup_logging.connect
def config_logger(*args, **kwargs):
    from logging.config import dictConfig
    from django.conf import settings
    dictConfig(settings.LOGGING)


app.autodiscover_tasks()


app.conf.beat_schedule = {
    "read-file-every_minute": {
        "task": "core.tasks.read_file_task",
        "schedule": crontab(),
    },
}
