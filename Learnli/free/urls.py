from django.urls import path
from .import views

 
urlpatterns=[
 # creating courses, course_units and lessons
    path("create_free_course",views.create_free_course, name='create_free_course'),
    path('enroll/<int:pk>',views.Enrolling, name='enroll'),
    path("create_course_unit",views.create_course_unit, name='create_course_unit'),
    path("create_free_lesson",views.create_free_lesson, name='create_free_lesson'),
    # showing classes, subjects and lessons
    path("courses",views.courses, name='courses'),
    path("myfree_courses",views.myfree_courses, name='my_free_courses'),
    path("course_units",views.course_units, name='course_units'),
    path("free_lessons",views.free_lessons, name='free_lessons'),
    # capturin subjects and lessons for each class and subject respectively
    path('course_course_units/<int:course_id>/course_units/',views.course_course_units,name='course_course_units'),
    path('course_units_lessons/<int:course_units_id>/lessons/',views.course_units_lessons,name='course_unit_lessons'),
    #editing classes, subjects and lessons
    path('edit_course/<course_id>',views.edit_course, name='edit_course'),
    path('edit_course_units/<course_units_id>',views.edit_course_units, name='edit_course_units'),
    path('edit_lesson/<lesson_id>',views.edit_lesson, name='edit_lesson'),
    #deleting classes, subjects and lessons
    path('delete_course/<course_id>',views.delete_course, name='delete_course'),
    path('delete_course_units/<course_units_id>',views.delete_course_units, name='delete_course_units'),
    path('delete_lesson/<lesson_id>',views.delete_lesson, name='delete_lesson'),
    
  
    ]