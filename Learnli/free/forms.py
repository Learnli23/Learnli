from django import forms
from django.forms import ModelForm
from .models import Course,Lessons,course_unit
from ckeditor.widgets import CKEditorWidget

# **FORMS THAT HANDLE CLASSES, SUBJECTS AND LESSONS**

# The Form that is used to add  and Edit Classes
class create_courseForm(ModelForm):
    level = forms.CharField(label='', widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"Enter level"}))
    title = forms.CharField(label='', widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"Class title"})) 
    image = forms.ImageField( )
    description = forms.Textarea( attrs = {'class':"enrollist","placeholder":"Description",})
    teacher = forms.Select(attrs = {'class':"form-select","placeholder":"creator",})
    with_course_units = forms.SelectMultiple(attrs = {'class':"form-control","placeholder":"sbjects",})
    
    class Meta:
        model=Course 
        fields = ['title','category','image','description','level','with_course_units','Duration']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        super().__init__(*args, **kwargs)
        if user:
            # Filter the with_subjects queryset to include only subjects created by the user
            self.fields['with_course_units'].queryset = course_unit.objects.filter(unit_teacher=user)    






# The Form that is used to add  and Edit subjects
class create_course_unitForm(ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"subject title"})) 
    image = forms.ImageField( )
    description = forms.Textarea( attrs = {'class':"enrollist","placeholder":"Description",})
    unit_teacher = forms.Select(attrs = {'class':"form-select","placeholder":"creator",})
    with_lessons = forms.SelectMultiple(attrs = {'class':"form-control","placeholder":"sbjects",})

     
    class Meta:
        model=course_unit  
        fields = ['title','image','description','with_lessons']


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        super().__init__(*args, **kwargs)
        if user:
            # Filter the with_lessons queryset to include only lessons created by the user
            self.fields['with_lessons'].queryset = Lessons.objects.filter(lesson_teacher=user)     
              

# The Form that is used to add  and Edit lessons
class create_lessonForm(ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"subject title"})) 
    power= forms.CharField(label='', widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"position"}))  
    taught_by = forms.Select(attrs = {'class':"form-select","placeholder":"teacher",})
    
     
    class Meta:
        model=Lessons  
        fields = ['title','video','notes','display_image','transcript_file','subtitle_file']  