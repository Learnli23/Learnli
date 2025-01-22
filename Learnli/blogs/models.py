
# Create your models here.
from django.db import models
from django.contrib.auth.models import User 
from users.models import user_Profile
from ckeditor.fields import RichTextField

# Create your models here.
#*****MODEELS TO HANDLe BLOGGS*******
   
class BlogPost(models.Model):
    author = models.ForeignKey(user_Profile, on_delete=models.CASCADE)
    author_title = models.CharField(max_length=200)
    blog_title = models.CharField(max_length=200)
    content = RichTextField()
    image = models.ImageField(upload_to='blog_images', blank=True, null=True)
    video = models.FileField(upload_to='blog_videos', blank=True, null=True)
    likes = models.ManyToManyField(user_Profile, related_name='blog_likes', blank=True)
    dislikes = models.ManyToManyField(user_Profile, related_name='blog_dislikes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reported = models.BooleanField(default=False)
    is_hiden = models.BooleanField(default=False)
     
    def __str__(self):
       return  f"{self. blog_title + '  ' + 'by'+ '  ' + str(self. author) }"

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

 



class Comment(models.Model):
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(user_Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.blog_title}'       
