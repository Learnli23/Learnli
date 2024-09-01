from django.urls import path
from .import views

 
urlpatterns=[
 # creating classes, subjects and lessons
    path("create_class",views.create_class, name='create_class'),
    path('enroll/<int:pk>',views.Enrolling, name='enroll'),
    path("create_subject",views.create_subject, name='create_subject'),
    path("create_lesson",views.create_lesson, name='create_lesson'),
    # showing classes, subjects and lessons
    path("classes",views.classes, name='classes'),
    path("my_courses",views.my_courses, name='my_courses'),
    path("subjects",views.subjects, name='subjects'),
    path("lessons",views.lessons, name='lessons'),
    # capturin subjects and lessons for each class and subject respectively
    path('class_subjects/<int:class_id>/subjects/',views.class_subjects,name='class_subjects'),
    path('subject_lessons/<int:subject_id>/lessons/',views.subject_lessons,name='subject_lessons'),
    #editing classes, subjects and lessons
    path('edit_class/<klass_id>',views.edit_class, name='edit_class'),
    path('edit_subject/<subject_id>',views.edit_subject, name='edit_subject'),
    path('edit_lesson/<lesson_id>',views.edit_lesson, name='edit_lesson'),
    #deleting classes, subjects and lessons
    path('delete_class/<klass_id>',views.delete_class, name='delete_class'),
    path('delete_subject/<subject_id>',views.delete_subject, name='delete_subject'),
    path('delete_lesson/<lesson_id>',views.delete_lesson, name='delete_lesson'),
    ]
