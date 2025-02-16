from django.contrib import admin
from . models import Lessons, Course,course_unit
# Register your models here.
admin.site.register(Lessons)
admin.site.register(course_unit)
admin.site.register(Course)
 