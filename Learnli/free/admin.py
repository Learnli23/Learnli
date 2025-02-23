from django.contrib import admin
from . models import Lessons, Course,course_unit,FreeSection,FreeContent,FreeEbook,FreeSub_Section
# Register your models here.
admin.site.register(Lessons)
admin.site.register(course_unit)
admin.site.register(Course)
admin.site.register(FreeContent)
admin.site.register(FreeEbook)
admin.site.register(FreeSection)
admin.site.register(FreeSub_Section)

 