import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Каждый вторник в 6 утра запускаем таски обновления ключей фнс и информации по всем компаниям
app.conf.beat_schedule = {
    'check_limit_key_fns': {
        'task': 'apps.api.tasks.check_limit_key_fns',
        'schedule': crontab(day_of_week=2, hour=8)
    },
    'api_to_fns_update': {
        'task': 'apps.api.tasks.api_to_fns_update',
        'schedule': crontab(day_of_week=2, hour=8)
    }
}

