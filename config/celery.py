import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Celery Beat - Periodic Tasks
app.conf.beat_schedule = {
    'clear-sessions-every-midnight': {
        'task': 'shop.tasks.clear_expired_sessions',
        'schedule': crontab(hour=0, minute=0),
    },
}