from django.db import models
from django.contrib.auth.models import User
from users.models import user_Profile
from ckeditor.fields import RichTextField
from django.utils import timezone


# Create your models here.
class Message(models.Model):
    sender =models.ForeignKey(user_Profile,related_name='sender',on_delete=models.CASCADE)
    reciepient =models.ForeignKey(user_Profile,related_name='reciepient',on_delete=models.CASCADE)
    content =RichTextField()
    timestamp =models.DateTimeField(auto_now_add=True)
    is_read =models.BooleanField(default=False)
    def __str__(self):
        return  f" message from {self.sender}"

# charts to us
 
class ContactMessage(models.Model):
    name =models.ForeignKey(user_Profile,related_name='sender_name',on_delete=models.CASCADE)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"


# Reminder
 
class CalendarEvent(models.Model):
    user = models.ForeignKey(user_Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateTimeField()
    notify = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title       