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
    taught_by =models.ForeignKey(user_Profile,on_delete= models.CASCADE,null=True)
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
class Subjects(models.Model):
    title =models.CharField(max_length=200)
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
    level = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = RichTextField()
    image = models.ImageField(null = True, blank = True, upload_to ="media")
    created_by =models.ForeignKey(user_Profile,on_delete= models.CASCADE)
    with_subjects = models.ManyToManyField(Subjects,symmetrical=False,blank=True)
    Enroll = models.ManyToManyField(user_Profile,related_name = 'enrolled_in', symmetrical = False, blank = True)
    Duration = models.CharField(max_length=200)
    created_on =models.DateField(auto_now=True)
    category = models.CharField(max_length=200, choices=CATEGORY)
    price = models.DecimalField(max_digits=10, decimal_places=2)  #field for price
    language = models.CharField(max_length=50, blank=True, null=True)  # Optional field for language
    paid_users = models.ManyToManyField(user_Profile,related_name='paid_course', blank=True)  # Track paid users
    reported = models.BooleanField(default=False)
    is_hiden = models.BooleanField(default=False)


    def __str__(self):
       return  f"{self.title}"


# Recommendations models
#user  recommendations(suggestions for similar content and persons)
class UserCourseActivity(models.Model):
    user = models.ForeignKey(user_Profile, on_delete=models.CASCADE)
    course = models.ForeignKey(Classes , on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50, choices=[('enrolled', 'Enrolled'), ('liked', 'Liked'), ('completed', 'Completed')])
    timestamp = models.DateTimeField(auto_now_add=True)

class UserBookActivity(models.Model):
    user = models.ForeignKey(user_Profile, on_delete=models.CASCADE)
    book = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50, choices=[('read', 'Read'), ('liked', 'Liked'), ('downloaded', 'Downloaded')])
    timestamp = models.DateTimeField(auto_now_add=True)

class UserTeacherActivity(models.Model):
    user = models.ForeignKey(user_Profile, on_delete=models.CASCADE)
    teacher = models.ForeignKey(user_Profile, related_name='recommended_teachers', on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50, choices=[('followed', 'Followed'), ('liked', 'Liked')])
    timestamp = models.DateTimeField(auto_now_add=True)