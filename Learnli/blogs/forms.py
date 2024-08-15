from django import forms
from django.forms import ModelForm
from .models import Comment,BlogPost

class CommentForm(forms.ModelForm):
       class Meta:
           model = Comment
           fields = ['content'] 

class BlogForm(ModelForm):
   #author = forms.Select(attrs = {'class':"form-select","placeholder":" author ",})
   author_title= forms.TextInput(attrs = {'class':"form-select","placeholder":"author_title",})
   blog_title = forms.TextInput(attrs = {'class':"form-select","placeholder":" blog_title",})
   content = forms.Textarea(attrs = {'class':"form-select","placeholder":" Enter content",})
   image = forms.ImageField()
   video = forms.FileInput()
    
    
    
   class Meta:
        model = BlogPost
        fields =['author_title','blog_title','content','image','video']     