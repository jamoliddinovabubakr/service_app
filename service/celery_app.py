import os
from celery import Celery
from django.conf import settings 


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')


app = Celery('service')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


import time

@app.task()
def debug_task():
    time.sleep(20)
    print('hello from debug_task')
