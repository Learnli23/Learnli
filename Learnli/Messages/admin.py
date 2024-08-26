from django.contrib import admin
from . models import Message,ContactMessage,CalendarEvent

# Register your models here.
admin.site.register(Message)
admin.site.register(ContactMessage)
admin.site.register(CalendarEvent)
