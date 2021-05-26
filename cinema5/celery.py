import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema5.settings')

app = Celery('cinema5')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()