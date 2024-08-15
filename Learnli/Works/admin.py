from django.contrib import admin
from . models import Lessons,Subjects,Classes
# Register your models here.
admin.site.register(Lessons)
admin.site.register(Subjects)
admin.site.register(Classes)
