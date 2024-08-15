from celery import shared_task
from django.core.management import call_command
import logging
logger = logging.getLogger(__name__)


@shared_task
def fetch_daily_nav():
    try:
        print("Running fetch_daily_nav task...")
        call_command('fetch_nav_data')
    except Exception as e:
        print(f"Error in fetch_daily_nav: {str(e)}")
        # You might want to log this error or raise it again

