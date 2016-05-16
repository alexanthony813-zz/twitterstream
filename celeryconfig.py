from celery.schedules import crontab

#used to schedule tasks periodically and passing optional arguments
#Can be very useful. Celery does not seem to support scheduled task but only periodic
CELERYBEAT_SCHEDULE = {
    'every-minute': {
        'task': 'tasks.sent',
        'schedule': crontab(minute='*/1'),
        'args': (1,2),
    },
}
