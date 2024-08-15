from django.forms import ModelForm
from .models import Message
from django import forms
 

class composeForm(ModelForm):
   sender = forms.Select(attrs = {'class':"form-select","placeholder":"sender",})
   reciepient =  forms.Select(attrs = {'class':"form-select","placeholder":"reciepient",})
   content = forms.Textarea( attrs = {'class':"enrollist","placeholder":"Description",})
   class Meta:
        model = Message
        fields =['reciepient','content',]
