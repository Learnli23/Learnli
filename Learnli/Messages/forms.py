from django.forms import ModelForm
from .models import Message,ContactMessage,CalendarEvent
from django import forms

 

class composeForm(ModelForm):
   sender = forms.Select(attrs = {'class':"form-select","placeholder":"sender",})
   reciepient =  forms.Select(attrs = {'class':"form-select","placeholder":"reciepient",})
   content = forms.Textarea( attrs = {'class':"enrollist","placeholder":"Description",})
   class Meta:
        model = Message
        fields =['reciepient','content',]



class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['message']   

# Reminder


class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['title', 'description', 'event_date', 'notify']
        widgets = {
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }             
