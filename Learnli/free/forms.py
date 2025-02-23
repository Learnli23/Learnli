from django import forms
from django.forms import ModelForm
from .models import Course,Lessons,course_unit,FreeContent,FreeEbook,FreeSection,FreeSub_Section
from ckeditor.widgets import CKEditorWidget

# **FORMS THAT HANDLE CLASSES, SUBJECTS AND LESSONS**

# The Form that is used to add  and Edit Classes
class create_courseForm(ModelForm):
    level = forms.CharField(label='', widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"Enter level"}))
    title = forms.CharField(label='', widget=forms.TextInput(attrs = {'class':"form-control","placeholder":"Course title"})) 
    image = forms.ImageField( )
    description = forms.Textarea( attrs = {'class':"enrollist","placeholder":"Description",})
    teacher = forms.Select(attrs = {'class':"form-select","placeholder":"creator",})
    with_course_units = forms.SelectMultiple(attrs = {'class':"form-control","placeholder":"course unit",})
    
    class Meta:
        model=Course 
        fields = ['title','category','image','description','level','with_course_units','Duration']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        super().__init__(*args, **kwargs)
        if user:
            # Filter the with_course_units queryset to include only subjects created by the user
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

    class Meta:
        model=Lessons  
        fields = ['title','video','notes','display_image','transcript_file','subtitle_file']  


#Library forms
class FreeContentForm(forms.ModelForm):
    class Meta:
        model = FreeContent
        fields = ['title', 'description', 'content_type', 'video','Audeo','paper_file','display_image',]

#Ebook forms

class FreeEbookForm(forms.ModelForm):
    class Meta:
        model = FreeEbook
        fields = ['title', 'description', 'display_image','ISBN','pages','language']
        Widget = {
            'title':CKEditorWidget(), 'description':CKEditorWidget(), 'display_image':CKEditorWidget(),'ISBN':CKEditorWidget()
        }
   


class FreeSectionForm(forms.ModelForm):
    class Meta:
        model = FreeSection
        fields = ['title', 'content', 'section_image','section_video']
        Widgets ={ 
            'title':CKEditorWidget(),'content': CKEditorWidget(),'section_image':CKEditorWidget(),'section_video':CKEditorWidget(),
          
        }
        

class Freesub_SectionForm(forms.ModelForm):
    class Meta:
        model = FreeSub_Section
        fields = ['title', 'content', 'section_image',"section_video"]
        Widgets ={ 
            'title':CKEditorWidget(),'content': CKEditorWidget(),'section_image':CKEditorWidget(),'section_video':CKEditorWidget(),
          
        }

        