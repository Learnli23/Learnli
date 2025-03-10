from django import forms
from django.forms import ModelForm
from .models import Classes,Lessons,Subjects
from ckeditor.widgets import CKEditorWidget

# **FORMS THAT HANDLE CLASSES, SUBJECTS AND LESSONS**

# The Form that is used to add  and Edit Classes
class create_classForm(ModelForm):
    level = forms.CharField(label='', widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"Enter level"}))
    title = forms.CharField(label='', widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"Class title"})) 
    image = forms.ImageField( )
    description = forms.Textarea( attrs = {'class':"enrollist","placeholder":"Description",})
    created_by = forms.Select(attrs = {'class':"form-select","placeholder":"creator",})
    with_subjects = forms.SelectMultiple(attrs = {'class':"form-control","placeholder":"sbjects",})
    
    class Meta:
        model=Classes  
        fields = ['title','category','image','description','level','with_subjects','Duration']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        super().__init__(*args, **kwargs)
        if user:
            # Filter the with_subjects queryset to include only subjects created by the user
            self.fields['with_subjects'].queryset = Subjects.objects.filter(taught_by=user)    






# The Form that is used to add  and Edit subjects
class create_subjectForm(ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"subject title"})) 
    image = forms.ImageField( )
    description = forms.Textarea( attrs = {'class':"enrollist","placeholder":"Description",})
   # created_on = forms.TextInput(attrs = {'class':"form-control","placeholder":"Date",})
    #image = forms.CharField(label='select an image', widget=forms.ClearableFileInput( attrs = {'class':"custom-file-input"}))
    taught_by = forms.Select(attrs = {'class':"form-select","placeholder":"creator",})
    with_lessons = forms.SelectMultiple(attrs = {'class':"form-control","placeholder":"sbjects",})

     
    class Meta:
        model=Subjects  
        fields = ['title','image','description','with_lessons']


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        super().__init__(*args, **kwargs)
        if user:
            # Filter the with_lessons queryset to include only lessons created by the user
            self.fields['with_lessons'].queryset = Lessons.objects.filter(taught_by=user)     
              

# The Form that is used to add  and Edit lessons
class create_lessonForm(ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"subject title"})) 
    power= forms.CharField(label='', widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"position"}))  
    taught_by = forms.Select(attrs = {'class':"form-select","placeholder":"teacher",})
    
     
    class Meta:
        model=Lessons  
        fields = ['title','video','notes','display_image','transcript_file','subtitle_file']         