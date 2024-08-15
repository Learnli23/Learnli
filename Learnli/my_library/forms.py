from django import forms
from .models import Content, Reaction,Ebook,Section,Sub_Section,Reviews
from ckeditor.widgets import CKEditorWidget

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'description', 'content_type', 'video','Audeo','paper_file','display_image',]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ['text']







#Ebook forms

class EbookForm(forms.ModelForm):
    class Meta:
        model = Ebook
        fields = ['title', 'description', 'display_image','ISBN']
        Widget = {
            'title':CKEditorWidget(), 'description':CKEditorWidget(), 'display_image':CKEditorWidget(),'ISBN':CKEditorWidget()
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['text']        


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['title', 'content', 'section_image','section_video']
        Widgets ={ 
            'title':CKEditorWidget(),'content': CKEditorWidget(),'section_image':CKEditorWidget(),'section_video':CKEditorWidget(),
          
        }
        

class sub_SectionForm(forms.ModelForm):
    class Meta:
        model = Sub_Section
        fields = ['title', 'content', 'section_image',"section_video"]
        Widgets ={ 
            'title':CKEditorWidget(),'content': CKEditorWidget(),'section_image':CKEditorWidget(),'section_video':CKEditorWidget(),
          
        }

