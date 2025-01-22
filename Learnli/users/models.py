from django.db import models
from django.contrib.auth.models import User 
from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.timezone import now, timedelta
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

 
# create your models here
 
# ***** MODEL TO HANDLE USERS****
class  user_Profile(AbstractUser):
    phone = models.CharField(max_length=200,blank=True)
    school =models.CharField(max_length=200,blank =True)
    major =models.CharField(max_length=200,blank =True)
    subject =models.CharField(max_length=200,blank =True)
    contact = models.CharField(max_length=200,blank =True)
    location =models.CharField(max_length=200,blank =True)
    website =models.URLField(max_length=200,blank=True)
    follows = models.ManyToManyField('self',related_name = 'followed_by', symmetrical = False, blank = True)
    date_modified = models.DateTimeField(User,auto_now = True)
    profile_image = models.ImageField(null = True, blank = True, upload_to ="media/") 
    is_student = models.BooleanField(default =False)
    is_teacher = models.BooleanField(default = False)
    is_institution = models.BooleanField(default = False)
    #content moderatioin
    is_content_moderation_agent = models.BooleanField(default = False)
    is_content_moderation_reviewer = models.BooleanField(default = False)
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


   
#model to store flagged content
class FlaggedContent(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Link to any model
    object_id = models.PositiveIntegerField()  # ID of the flagged object
    content_object = GenericForeignKey('content_type', 'object_id')  # Access the actual object
    reported_by = models.ForeignKey(user_Profile, on_delete=models.CASCADE, related_name="flagged_content")
    reason = models.TextField()
    date_reported = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)
    approved = models.BooleanField(null=True, blank=True)  # True if approved, False if rejected
    escalated = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

     # Automatically store the model name for filtering and display
    @property
    def content_category(self):
        return self.content_type.model.capitalize()  # e.g., 'blog', 'course' -> 'Blog', 'Course'
     

    def __str__(self):
        return f"Flagged: {self.content_object} by {self.reported_by}"  
    
    


    


 

 

 

