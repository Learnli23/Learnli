from django.db import models
from users.models import user_Profile
from ckeditor.fields import RichTextField
from my_library.models  import Ebook

# Create your models here.
#*****MODEELS TO HANDLE TEACHER CONTENT*******
  # model to hundle the lessons
class Lessons(models.Model):
    title =models.CharField(max_length=200) 
    power = models.CharField(max_length=11) 
    position =models.IntegerField(blank=True,null=True)
    created_on =models.DateField(auto_now_add=True)
    lesson_teacher =models.ForeignKey(user_Profile,related_name = 'taecher',on_delete= models.CASCADE,null=True)
    notes = models.FileField(upload_to='notes/')
    video = models.FileField(upload_to='video/')
    display_image = models.ImageField(null = True, blank = True, upload_to ="media")
    subtitle_file = models.FileField(upload_to='subtitles/', blank=True, null=True)
    transcript_file = models.FileField(upload_to='transcripts/', blank=True, null=True)
    reported = models.BooleanField(default=False)
    is_hiden = models.BooleanField(default=False)
    
     
    def __str__(self):
       return  f"{self.title}"

 # model to hundel the  subjects
class course_unit(models.Model):
    title =models.CharField(max_length=200)
    description = RichTextField()
    created_on =models.DateField(auto_now=True)
    image = models.ImageField(null = True, blank = True, upload_to ="media")
    with_lessons =models.ManyToManyField(Lessons,symmetrical=False,blank=True,related_name='course_unit')
    unit_teacher =models.ForeignKey(user_Profile,on_delete= models.CASCADE)
    

    def __str__(self):
       return  f"{self.title}"

# model to hundel the classs
class Course(models.Model):
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
    level = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = RichTextField()
    image = models.ImageField(null = True, blank = True, upload_to ="media")
    teacher =models.ForeignKey(user_Profile,on_delete= models.CASCADE)
    with_course_units = models.ManyToManyField(course_unit,symmetrical=False,blank=True)
    Enroll = models.ManyToManyField(user_Profile,related_name = 'enrolled', symmetrical = False, blank = True)
    Duration = models.CharField(max_length=200)
    created_on =models.DateField(auto_now=True)
    category = models.CharField(max_length=200, choices=CATEGORY)
    language = models.CharField(max_length=50, blank=True, null=True)  # Optional field for language
    reported = models.BooleanField(default=False)
    is_hiden = models.BooleanField(default=False)


    def __str__(self):
       return  f"{self.title}"


 #uploaded books,articles,videos,audios

class FreeContent(models.Model):
    CONTENT_TYPES = [
        ('book', 'Book'),
        ('article', 'Article'),
        ('video', 'Video'),
        ('Audeo', 'Audeo'),
    ]

    title = models.CharField(max_length=200)
    creator = models.ForeignKey(user_Profile, on_delete=models.CASCADE)
    description = RichTextField()
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    display_image = models.FileField(upload_to='content/',blank=True)
    video = models.FileField(upload_to='content/',blank=True)
    Audeo = models.FileField(upload_to='content/',blank=True)
    paper_file = models.FileField(upload_to='content/',blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=50, blank=True, null=True)  # Optional field for language
    reported = models.BooleanField(default=False)
    is_hiden = models.BooleanField(default=False)

    def __str__(self):
        return self.title


#Ebook models
class FreeEbook(models.Model):
    title = models.CharField(max_length=200)
    creator =models.ForeignKey(user_Profile,related_name='creator', on_delete=models.CASCADE)
    description = RichTextField()
    display_image = models.ImageField(upload_to = 'display_images/',null=True)
    date_updated = models.DateField(auto_now=True)
    ISBN = models.CharField(max_length=200,blank=True)
    language = models.CharField(max_length=50, blank=True, null=True)  # Optional field for language
    pages = models.PositiveIntegerField(blank=True, null=True)  # Optional field for pages
    reported = models.BooleanField(default=False)
    is_hiden = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class FreeSection(models.Model):
    Freeebook = models.ForeignKey(FreeEbook, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextField()
    section_image = models.ImageField(upload_to = 'images/',null =True,blank=True)
    section_video =models.FileField(upload_to='content/',blank=True)
    section_creator =models.ForeignKey(user_Profile,related_name='section_creator', on_delete=models.CASCADE,null=True,blank =True)

    def __stsr__(self):
        return self.title


class FreeSub_Section(models.Model):
    section = models.ForeignKey(FreeSection, related_name='sub_sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextField()
    section_image = models.ImageField(upload_to = 'images/',null =True,blank=True)
    section_video =models.FileField(upload_to='content/',blank=True,null =True)
    subsection_creator =models.ForeignKey(user_Profile,related_name='subsection_creator', on_delete=models.CASCADE,null=True,blank =True)

    def __stsr__(self):
        return self.title        
