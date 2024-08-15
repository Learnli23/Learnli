from django.db import models
from django.contrib.auth.models import User
from users.models import user_Profile
from ckeditor.fields import RichTextField

# Create your models here.
class Message(models.Model):
    sender =models.ForeignKey(user_Profile,related_name='sender',on_delete=models.CASCADE)
    reciepient =models.ForeignKey(user_Profile,related_name='reciepient',on_delete=models.CASCADE)
    content =RichTextField()
    timestamp =models.DateTimeField(auto_now_add=True)
    is_read =models.BooleanField(default=False)
    def __str__(self):
        return  f" message from {self.sender}"

