import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ems.settings')

app = Celery('ems')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'fetch-daily-nav': {
        'task': 'apis.tasks.fetch_daily_nav',
        'schedule': crontab(hour=19, minute=30),
    },
}
