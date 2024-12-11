from django import forms
from django.forms import ModelForm
from .models import Exam, Answer,Test,Test_answer,RegisterforExam,Test_answer_response,Exam_answer_response
from django import forms


class ExamForm(ModelForm):
   Cours_name = forms.Select(attrs = {'class':"form-select","placeholder":" Cours_name ",})
   Examination_name= forms.TextInput(attrs = {'class':"form-select","placeholder":"Examination name",})
   semester = forms.TextInput(attrs = {'class':"form-select","placeholder":" semester",})
   instructins = forms.TextInput(attrs = {'class':"form-select","placeholder":" Enter instructions",})
   Duration = forms.TextInput(attrs = {'class':"form-select","placeholder":" Duration ",})
   Question = forms.Textarea(attrs = {'class':"form-select","placeholder":" Type Questions... ",})
   created_by =forms.Select(attrs = {'class':"form-select","placeholder":" created by ",})

    
    
   class Meta:
        model = Exam
        fields =['Cours_name','Examination_name','semester','instructins','Duration','Question','release']



class RegisterforExamForm(ModelForm):
 
   exam =forms.Select(attrs = {'class':"form-select","placeholder":" created by ",})
   

   class Meta:
        model = RegisterforExam
        fields =['exam',]        



class AnswerForm(ModelForm):
   Cours_name = forms.Select(attrs = {'class':"form-select","placeholder":" Cours_name ",})
   Examination_name= forms.Select(attrs = {'class':"form-select","placeholder":" Examination_name ",})
   semester = forms.TextInput(attrs = {'class':"form-select","placeholder":" semester",})
   Answered_by =forms.Select(attrs = {'class':"form-select","placeholder":" Answered by ",})
   Answered_to =forms.Select(attrs = {'class':"form-select","placeholder":" Answered to ",})
   text = forms.Textarea(attrs = {'class':"form-select","placeholder":" Type Answers... ",})
   
   class Meta:
        model = Answer
        fields =['text']        





class TestForm(ModelForm):
   Subject_name = forms.Select(attrs = {'class':"form-select","placeholder":" Subject name ",})
   semester = forms.TextInput(attrs = {'class':"form-select","placeholder":" semester",})
   instructins = forms.TextInput(attrs = {'class':"form-select","placeholder":" Enter instructions",})
   Duration = forms.TextInput(attrs = {'class':"form-select","placeholder":" Duration ",})
   Question = forms.Textarea(attrs = {'class':"form-select","placeholder":" Type Questions... ",})
   created_by =forms.Select(attrs = {'class':"form-select","placeholder":" created by ",})

   class Meta:
        model = Test
        fields =['Subject_name','semester','instructins','Duration','Question','release',]   



class Test_answerForm(ModelForm):
   Subject = forms.Select(attrs = {'class':"form-select","placeholder":" Subject name ",})
   semester = forms.TextInput(attrs = {'class':"form-select","placeholder":" semester",})
   Answered_by =forms.Select(attrs = {'class':"form-select","placeholder":" Answered by ",})
   Answered_to =forms.Select(attrs = {'class':"form-select","placeholder":" Answered to ",})
   text = forms.Textarea(attrs = {'class':"form-select","placeholder":" Type Answers... ",})
   
   class Meta:
        model = Test_answer
        fields =['text']              


class Test_answer_responseForm(ModelForm):
   Subject = forms.Select(attrs = {'class':"form-select","placeholder":" Subject name ",})
   semester = forms.TextInput(attrs = {'class':"form-select","placeholder":" semester",})
   response_by =forms.Select(attrs = {'class':"form-select","placeholder":" Answered by ",})
   answer =forms.Select(attrs = {'class':"form-select","placeholder":" Answeres ",})
   response_to =forms.Select(attrs = {'class':"form-select","placeholder":" Answered to ",})
   marks = forms.IntegerField()
   General_comment = forms.Textarea(attrs = {'class':"form-select","placeholder":" Type comments.. ",})
   class Meta:
        model =  Test_answer_response
        fields =['marks','General_comment']



 

class Exam_answer_responseForm(ModelForm):
   Course = forms.Select(attrs = {'class':"form-select","placeholder":" Course name ",})
   semester = forms.TextInput(attrs = {'class':"form-select","placeholder":" semester",})
   responseby =forms.Select(attrs = {'class':"form-select","placeholder":" Answered by ",})
   Examination =forms.Select(attrs = {'class':"form-select","placeholder":" Examination ",})
   responseto=forms.Select(attrs = {'class':"form-select","placeholder":" Answered to ",})
   scores = forms.IntegerField()
   Generalcomment = forms.Textarea(attrs = {'class':"form-select","placeholder":" Type comments.. ",})
   class Meta:
        model =  Exam_answer_response
        fields =['scores','Generalcomment']