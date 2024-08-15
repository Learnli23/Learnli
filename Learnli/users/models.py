from django.db import models
from django.contrib.auth.models import User 
from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.db.models.signals import post_save
from django.conf import settings
# create your models here
 
# ***** MODEL TO HANDLE USERS****
class  user_Profile(AbstractUser):
    phone = models.CharField(max_length=1000,blank=True)
    school =models.CharField(max_length=1000,blank =True)
    major =models.CharField(max_length=1000,blank =True)
    subject =models.CharField(max_length=1000,blank =True)
    contact = models.CharField(max_length=1000,blank =True)
    location =models.CharField(max_length=1000,blank =True)
    website =models.URLField(max_length=1000,blank=True)
    follows = models.ManyToManyField('self',related_name = 'followed_by', symmetrical = False, blank = True)
    date_modified = models.DateTimeField(User,auto_now = True)
    profile_image = models.ImageField(null = True, blank = True, upload_to ="media/") 
    is_student = models.BooleanField(default =False)
    is_teacher = models.BooleanField(default = False)
    is_institution = models.BooleanField(default = False)

    def __str__(self):
        return  f"{self.username}"

    def save(self,*args,**kwargs):
        created = not self.pk
        super().save(*args,**kwargs)
        # if user is just created, make them follow themselves.
        if created:
            self.follows.add(self)
            self.save()
