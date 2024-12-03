from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm  
from django.forms import ModelForm
from django.db import transaction
from .models import User,user_Profile
from datetime import timedelta
from django.utils import timezone

class student_SignupForm(UserCreationForm  ):
    username = forms.CharField(label='', widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"Enter user name"}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"Email Address"})) 
    first_name = forms.CharField(label='', max_length =100, widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"first Name",}))   
    last_name = forms.CharField(label='', max_length =100, widget=forms.TextInput( attrs = {'class':"form-control","placeholder":"last Name",}))
    password1 = forms.CharField(label='', max_length =100, widget=forms.PasswordInput( attrs = {'class':"form-control","placeholder":" Enter password",}))
    password2 = forms.CharField(label='', max_length =100, widget=forms.PasswordInput( attrs = {'class':"form-control","placeholder":"Re-enter password",}))
    school =  forms.CharField(label='', max_length =100, widget=forms.TextInput( attrs = {'class':"form-control","placeholder":"school",}))   
    phone =  forms.CharField(label='', max_length =100, widget=forms.TextInput( attrs = {'class':"form-control","placeholder":"phone",}))
    profile_image =forms.ImageField()
    class Meta:
        model=get_user_model()  
        fields = ['username', 'first_name','last_name','email','school','phone','password1','password2','profile_image']

    @transaction.atomic 
    def save(self,commit=True):
        user = super().save(commit= False) 
        user.is_student = True
        user.subscription_start_dat = timezone.now()
        user.subscription_end_date= timezone.now() + timedelta(days=30)
        if commit:
           user.save() 
        return user

class teacher_SignupForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"Enter user name"}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"Email Address"})) 
    first_name = forms.CharField(label='', max_length =100, widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"first Name",}))   
    last_name = forms.CharField(label='', max_length =100, widget=forms.TextInput( attrs = {'class':"form-control","placeholder":"last Name",}))
    password1 = forms.CharField(label='', max_length =100, widget=forms.PasswordInput( attrs = {'class':"form-control","placeholder":" Enter password",}))
    password2 = forms.CharField(label='', max_length =100, widget=forms.PasswordInput( attrs = {'class':"form-control","placeholder":"Re-enter password",}))
    school =  forms.CharField(label='', max_length =100, widget=forms.TextInput( attrs = {'class':"form-control","placeholder":"school",}))   
    phone =  forms.CharField(label='', max_length =100, widget=forms.TextInput( attrs = {'class':"form-control","placeholder":"phone",}))
    subject =  forms.CharField(label='', max_length =100, widget=forms.TextInput( attrs = {'class':"form-control","placeholder":"sbuject",}))
    major =  forms.CharField(label='', max_length =100, widget=forms.TextInput( attrs = {'class':"form-control","placeholder":"major",}))
    profile_image =forms.ImageField()
    
    class Meta(UserCreationForm.Meta):
          model=get_user_model()  
          fields = ['username', 'first_name','last_name','email','school','phone','major','subject','password1','password2','profile_image']

    @transaction.atomic 
    def save(self,commit=True):
        user = super().save(commit= False) 
        user.is_teacher = True
        user.subscription_start_dat = timezone.now()
        user.subscription_end_date= timezone.now() + timedelta(days=30)
        if commit:
           user.save() 
        return user        


class institution_SignupForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"Enter user name"}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"Email Address"})) 
    contact = forms.CharField(label='', max_length =100, widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"contact",}))   
    website = forms.URLField(label='', max_length =100, widget=forms.TextInput( attrs = {'class':"form-control","placeholder":"website",}))
    location =  forms.CharField(label='', max_length =100, widget=forms.TextInput( attrs = {'class':"form-control","placeholder":"location",}))   
    phone =  forms.CharField(label='', max_length =100, widget=forms.TextInput( attrs = {'class':"form-control","placeholder":"phone",}))
    password1 = forms.CharField(label='', max_length =100, widget=forms.PasswordInput( attrs = {'class':"form-control","placeholder":" Enter password",}))
    password2 = forms.CharField(label='', max_length =100, widget=forms.PasswordInput( attrs = {'class':"form-control","placeholder":"Re-enter password",}))
    profile_image =forms.ImageField()
     
    class Meta:
         model=get_user_model() 
         fields = ['username','email','phone','website','location','contact','password1','password2','profile_image']

    @transaction.atomic 
    def save(self,commit=True):
        user = super().save(commit= False) 
        user.is_institution = True
        user.subscription_start_dat = timezone.now()
        user.subscription_end_date= timezone.now() + timedelta(days=30)
        if commit:
           user.save() 
        return user
    


# Form to select subscription length
class SubscriptionForm(forms.Form):
    
    # Options for subscription duration
    SUBSCRIPTION_LENGTHS = [
        (1, '1 Month'),
        (3, '3 Months'),
        (6, '6 Months'),
        (12, '12 Months'),
    ]
    CURRENCY_CHOICES = [
        ('USD', 'usa Dollar'), ('NGN', 'Nigerian Nira'),
        ('UGX', 'Uganda shillings'), ('KES', 'Kenyan Shillings'),('XAF','Central African CFA Franc'),('XOF','West African CFA Franc'),
        ('GBP','British Pound Sterling'),('EUR','Euro'),('ETB','Ethiopian Birr'),('ZMW','Zambian Kwacha'),('RWF','Rwandan Franc'),
        ('GHS','Ghanaian Cedi'),('ZAR','South African Rand'),('TZS','Tanzanian Shillings')

         
    ]

    subscription_type = forms.ChoiceField(choices=SUBSCRIPTION_LENGTHS, label='Choose your subscription type')  # Drop-down field for selecting length    
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES, label='Currency')

    class Meta:
         Model = model=get_user_model() 

class ReportContentForm(forms.Form):
      reason = forms.CharField(widget=forms.Textarea, label="Reason for reporting")