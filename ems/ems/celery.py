# celery.py

import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('your_project')

# Use a string here instead of a file path for a better configuration
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-nav-data-daily': {
        'task': 'your_app.tasks.daily_update_nav_data',
        'schedule': crontab(hour=1, minute=0),
    },
}