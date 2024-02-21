import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EasyGymCheckin.settings')

app = Celery('EasyGymCheckin')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'UTC'
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'test': {
        'task': 'test',
        'schedule': 60.0,
    },
    'syncClients': {
        'task': 'syncClients',
        'schedule': 400.0,
    },
    'syncClasses': {
        'task': 'syncClasses',
        'schedule': 300.0,
    },
}
