from django.db import models
from users.models import user_Profile
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here
#uploaded books,articles,videos,audios

class Content(models.Model):
    CONTENT_TYPES = [
        ('book', 'Book'),
        ('article', 'Article'),
        ('video', 'Video'),
        ('Audeo', 'Audeo'),
    ]

    title = models.CharField(max_length=200)
    author = models.ForeignKey(user_Profile, on_delete=models.CASCADE)
    description = RichTextField()
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    display_image = models.FileField(upload_to='content/',blank=True)
    video = models.FileField(upload_to='content/',blank=True)
    Audeo = models.FileField(upload_to='content/',blank=True)
    paper_file = models.FileField(upload_to='content/',blank=True)
    #price = models.DecimalField(max_digits=6, decimal_places=2)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Reaction(models.Model):
    content = models.ForeignKey(Content, related_name='comments', on_delete=models.CASCADE)
    Commenter = models.ForeignKey(user_Profile,related_name='commenter', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.Commenter} on {self.content.title}'


       


#Ebook models
class Ebook(models.Model):
    title = models.CharField(max_length=200)
    author =models.ForeignKey(user_Profile,related_name='author', on_delete=models.CASCADE)
    description = RichTextField()
    display_image = models.ImageField(upload_to = 'display_images/',null=True)
    date_updated = models.DateField(auto_now=True)
    ISBN = models.CharField(max_length=2000,blank=True)

    def __str__(self):
        return self.title


# book reviews
class Reviews(models.Model):
    ebook = models.ForeignKey(Ebook, related_name='reviews', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(user_Profile,related_name='reviewer', on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.reviewer} on {self.book.title}' 




class Section(models.Model):
    ebook = models.ForeignKey(Ebook, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextField()
    section_image = models.ImageField(upload_to = 'images/',null =True,blank=True)
    section_video =models.FileField(upload_to='content/',blank=True)
    section_author =models.ForeignKey(user_Profile,related_name='section_author', on_delete=models.CASCADE,null=True,blank =True)

    def __stsr__(self):
        return self.title


class Sub_Section(models.Model):
    section = models.ForeignKey(Section, related_name='sub_sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextField()
    section_image = models.ImageField(upload_to = 'images/',null =True,blank=True)
    section_video =models.FileField(upload_to='content/',blank=True,null =True)
    subsection_author =models.ForeignKey(user_Profile,related_name='subsection_author', on_delete=models.CASCADE,null=True,blank =True)

    def __stsr__(self):
        return self.title        
