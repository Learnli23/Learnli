from celery import shared_task
from django.core.mail import send_mail
from .models import CalendarEvent
from django.utils import timezone

@shared_task
def send_event_notifications():
    events = CalendarEvent.objects.filter(notify=True, event_date__gte=timezone.now())
    for event in events:
        # Check if the event is within a notification time window
        if event.event_date <= timezone.now() + timezone.timedelta(hours=1):
            send_mail(
                subject=f'Upcoming Event: {event.title}',
                message=f'Reminder: You have an upcoming event - {event.title} on {event.event_date}.',
                from_email='learnli759@gmail.com',
                recipient_list=[event.user.email],
            )
            event.notify = False  # Turn off notification after sending
            event.save()