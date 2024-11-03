from django.db import models
from django.contrib.auth.models import User 
from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.timezone import now, timedelta
from datetime import timedelta

 
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
    #  user Subscription fields
    subscription_active = models.BooleanField(default=False)
    subscription_start_date = models.DateTimeField(null=True, blank=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)
    subscription_type = models.CharField(max_length=10, choices=[('1_month', '1 Month'), ('3_months', '3 Months'), ('6_months', '6 Months'), ('1_year', '1 Year')], null=True, blank=True)
     # Payment-related field
    subscription_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    currency_choice = models.CharField(max_length=100, choices=[('USD', 'usa_Dollar'), ('NGN', 'Nigerian Nira'),
  ('UGX', 'Uganda shillings'), ('KES', 'Kenyan Shillings'),('XAF','Central African CFA Franc'),('XOF','West African CFA Franc'),
  ('GBP','British Pound Sterling'),('EUR','Euro'),('ETB','Ethiopian Birr'),('ZMW','Zambian Kwacha'),('RWF','Rwandan Franc'),
  ('GHS','Ghanaian Cedi'),('ZAR','South African Rand'),('TZS','Tanzanian Shillings')], null=True, blank=True)

    # class methods to carry out automated actions
    def __str__(self):
        return  f"{self.username}"

    def save(self,*args,**kwargs):
        created = not self.pk
        super().save(*args,**kwargs)
        # if user is just created, make them follow themselves.
        if created:
            self.follows.add(self)
            self.save()

    # method to check expired subscription 
    def check_subscription(self):
        if self.subscription_end_date and self.subscription_end_date <= now():
            self.subscription_active = False
            self.save()
        else:   
                self.subscription_active = True
                self.save()     
        return self.subscription_active        


   
 
     
 
  
    
    


    


 

 

 

