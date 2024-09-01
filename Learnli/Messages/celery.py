from celery import Celery

app = Celery('learnli')

app.conf.beat_schedule = {
    'send-event-notifications-every-hour': {
        'task': 'your_app.tasks.send_event_notifications',
        'schedule': 3600.0,  # Every hour
    },
}