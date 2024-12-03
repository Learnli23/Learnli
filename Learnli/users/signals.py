from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FlaggedContent

@receiver(post_save, sender=FlaggedContent)
def mark_content_as_reported(sender, instance, created, **kwargs):
    if created:
        instance.content_object.reported = True
        instance.content_object.save()