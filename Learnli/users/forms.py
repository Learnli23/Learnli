from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm  
from django.forms import ModelForm
from django.db import transaction
from .models import User

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
        if commit:
           user.save() 
        return user