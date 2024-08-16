import os
import django
import time
from apis.tasks import fetch_daily_nav
from celery.result import AsyncResult

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ems.settings')
django.setup()

if __name__ == '__main__':
    task = fetch_daily_nav.delay()
    print(f"Task ID: {task.id}")

    while True:
        result = AsyncResult(task.id)
        print(f"Task status: {result.status}")

        if result.ready():
            if result.successful():
                print(f"Task result: {result.get()}")
            else:
                print(f"Task failed: {result.result}")
            break

        time.sleep(1)
