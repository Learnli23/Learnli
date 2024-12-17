from django.db import models
from django.contrib.auth.models import User
from users.models import user_Profile
from Works.models import Subjects,Lessons,Classes
from ckeditor.fields import RichTextField

# Create your models here.
 


class Exam(models.Model):
    Cours_name = models.ForeignKey(Classes, on_delete=models.CASCADE,related_name='Cours_name')
    Examination_name =models.CharField(max_length=2550)
    semester = models.CharField(max_length=2550)
    Date =models.DateField(auto_now=True)
    instructins = RichTextField()
    Duration = models.IntegerField()
    Question = RichTextField()
    created_by  = models.ForeignKey(user_Profile, on_delete=models.CASCADE,related_name='created_by')
    release = models.BooleanField(default=False)
    candidates = models.ManyToManyField(user_Profile, related_name ="exam_registered")

    def __str__(self):
        return  f" {self.Examination_name} creeated by {self.created_by}"


class RegisterforExam(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE,related_name='Register')
    name = models.ForeignKey(user_Profile, on_delete=models.CASCADE,related_name='name')
    teacher = models.ForeignKey(user_Profile, on_delete=models.CASCADE,related_name='teacher')
    Registered_date =models.DateField(auto_now=True)
    def __str__(self):
        return  f"{self.name} registered for the {self.exam} "

class Answer(models.Model):
    Cours_name = models.ForeignKey(Classes, on_delete=models.CASCADE,related_name='Coursname')
    Examination_name =models.ForeignKey(Exam, on_delete=models.CASCADE,related_name='Examinationname')
    semester = models.CharField(max_length=2550)
    Date =models.DateField(auto_now=True)
    Answered_by = models.ForeignKey(user_Profile, on_delete=models.CASCADE,related_name='Answered_by')
    Answered_to = models.ForeignKey(user_Profile, on_delete=models.CASCADE,related_name='Answered_to',null=True)
    text = RichTextField()
    submitted_at =models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return  f" Answer submited by {self.Answered_by}"



class Exam_answer_response(models.Model):
   Course = models.ForeignKey(Classes, on_delete=models.CASCADE,related_name='course',null=True)
   Examination  = models.ForeignKey(Exam, on_delete=models.CASCADE,related_name='Exam',null=True)
   semester = models.CharField(max_length=255 )
   responseby = models.ForeignKey(user_Profile, on_delete=models.CASCADE,related_name='responseby')
   responseto = models.ForeignKey(user_Profile, on_delete=models.CASCADE,related_name='responseto',null=True)
   scores = models.IntegerField()
   Generalcomment = RichTextField()
   submittedat =models.DateTimeField(auto_now_add=True)
    
   def __str__(self):
        return  f" Response submited by {self.responseby} to {self.responseto} on {self.submittedat}"          
    

     
class Test(models.Model):
    Subject_name = models.ForeignKey(Subjects, on_delete=models.CASCADE,related_name='Subject_name',null=True)
    semester = models.CharField(max_length=2550)
    Date =models.DateField(auto_now=True)
    instructins = RichTextField()
    Duration = models.IntegerField()
    Question =RichTextField()
    created_by  = models.ForeignKey(user_Profile, on_delete=models.CASCADE,related_name='creatd_by')
    release = models.BooleanField(default=False)
     

    def __str__(self):
        return  f" Test creeated by {self.created_by}"
    



class Test_answer(models.Model):
    Subject_name = models.ForeignKey(Subjects, on_delete=models.CASCADE,related_name='Subjectname',null=True)
    semester = models.CharField(max_length=2550)
    Date =models.DateField(auto_now=True)
    Answered_by = models.ForeignKey(user_Profile, on_delete=models.CASCADE,related_name='Answere_given_by')
    Answered_to = models.ForeignKey(user_Profile, on_delete=models.CASCADE,related_name='Answeredto',null=True)
    text = RichTextField()
    submitted_at =models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return  f" Answer submited by {self.Answered_by}"



class Test_answer_response(models.Model):
    Subject = models.ForeignKey(Subjects, on_delete=models.CASCADE,related_name='Subject',null=True)
    answer = models.ForeignKey(Test_answer, on_delete=models.CASCADE,related_name='answer',null=True)
    semester = models.CharField(max_length=255 )
    response_by = models.ForeignKey(user_Profile, on_delete=models.CASCADE,related_name='response_by')
    response_to = models.ForeignKey(user_Profile, on_delete=models.CASCADE,related_name='response_to',null=True)
    marks = models.IntegerField()
    General_comment =RichTextField()
    submitted_at =models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return  f" Response submited by {self.response_by} to {self.response_to} on {self.submitted_at}"
