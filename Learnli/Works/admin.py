from django.contrib import admin
from . models import Lessons,Subjects,Classes,UserBookActivity,UserCourseActivity,UserTeacherActivity
# Register your models here.
admin.site.register(Lessons)
admin.site.register(Subjects)
admin.site.register(Classes)
admin.site.register(UserBookActivity)
admin.site.register(UserCourseActivity)
admin.site.register(UserTeacherActivity)
