from django.db import models
from users.models import user_Profile
from ckeditor.fields import RichTextField

# Create your models here.
#*****MODEELS TO HANDLE TEACHER CONTENT*******
  # model to hundle the lessons
class Lessons(models.Model):
    title =models.CharField(max_length=1000000) 
    power = models.CharField(max_length=11) 
    position =models.IntegerField(blank=True,null=True)
    created_on =models.DateField(auto_now_add=True)
    taught_by =models.ForeignKey(user_Profile,on_delete= models.CASCADE,null=True)
    notes = models.FileField(upload_to='notes/')
    video = models.FileField(upload_to='video/')
    display_image = models.ImageField(null = True, blank = True, upload_to ="media")
    subtitle_file = models.FileField(upload_to='subtitles/', blank=True, null=True)
    transcript_file = models.FileField(upload_to='transcripts/', blank=True, null=True)
    
     
    def __str__(self):
       return  f"{self.title}"

 # model to hundel the  subjects
class Subjects(models.Model):
    title =models.CharField(max_length=100000)
    description = RichTextField()
    created_on =models.DateField(auto_now=True)
    image = models.ImageField(null = True, blank = True, upload_to ="media")
    with_lessons =models.ManyToManyField(Lessons,symmetrical=False,blank=True)
    taught_by =models.ForeignKey(user_Profile,on_delete= models.CASCADE)
    

    def __str__(self):
       return  f"{self.title}"

# model to hundel the classs
class Classes(models.Model):
    CATEGORY = [
        ('science', 'science'),
        ('Arts', 'Arts'),
        ('Engineering', 'Engineering'),
        ('Business', 'Business'),
        ('creative_work','creative_work'),
        ('Languages','Languages'),
        ('computor_science','computer_science'),
        ('others','others'),
        ('Religios_studies','Religious_studies')
    ]
    level = models.CharField(max_length=1000000)
    title = models.CharField(max_length=1000000)
    description = RichTextField()
    image = models.ImageField(null = True, blank = True, upload_to ="media")
    created_by =models.ForeignKey(user_Profile,on_delete= models.CASCADE)
    with_subjects = models.ManyToManyField(Subjects,symmetrical=False,blank=True)
    Enroll = models.ManyToManyField(user_Profile,related_name = 'enrolled_in', symmetrical = False, blank = True)
    Duration = models.CharField(max_length=2000)
    created_on =models.DateField(auto_now=True)
    category = models.CharField(max_length=100000000, choices=CATEGORY)

    def __str__(self):
       return  f"{self.title}"
