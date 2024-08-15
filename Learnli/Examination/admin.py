from django.contrib import admin
from .models import Exam,Answer,Test,Test_answer,RegisterforExam,Test_answer_response,Exam_answer_response


# Register your models here.
admin.site.register(Answer)
admin.site.register(Exam)
admin.site.register(Test_answer)
admin.site.register(Test)
admin.site.register(RegisterforExam)
admin.site.register(Test_answer_response)
admin.site.register(Exam_answer_response)
