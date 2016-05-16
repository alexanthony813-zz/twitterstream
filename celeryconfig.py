from celery.schedules import crontab

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = "mongodb"
CELERY_RESULT_URI = "http://localhost:27017"
# CELERY_MONGODB_BACKEND_SETTINGS = {
#     "host": "127.0.0.1",
#     "port": 27017,
#     "database": "jobs",
#     "taskmeta_collection": "stock_taskmeta_collection",
# }

#used to schedule tasks periodically and passing optional arguments
#Can be very useful. Celery does not seem to support scheduled task but only periodic
# CELERYBEAT_SCHEDULE = {
#     'every-minute': {
#         'task': 'tasks.sent_analysis',
#         'schedule': crontab(minute='*/1'),
#         'args': (1,2),
#     },
# }
