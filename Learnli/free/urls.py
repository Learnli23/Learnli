from django.urls import path
from .import views

 
urlpatterns=[
 # creating courses, course_units and lessons
    path("create_free_course",views.create_free_course, name='create_free_course'),
    path('free_course_details/<int:pk>',views.free_course_details, name='free_course_details'),
    path("create_course_unit",views.create_course_unit, name='create_course_unit'),
    path("create_free_lesson",views.create_free_lesson, name='create_free_lesson'),
    # showing classes, subjects and lessons
    path("courses",views.courses, name='courses'),
    path("myfree_courses",views.myfree_courses, name='my_free_courses'),
    path("course_units",views.course_units, name='course_units'),
    path("free_lessons",views.free_lessons, name='free_lessons'),
    # capturin subjects and lessons for each class and subject respectively
    path('course_course_units/<int:course_id>/course_units/',views.course_course_units,name='course_course_units'),
    path('course_unit_lessons/<int:course_unit_id>/lessons/',views.course_unit_lessons,name='course_unit_lessons'),
    #editing classes, subjects and lessons
    path('edit_course/<course_id>',views.edit_course, name='edit_course'),
    path('edit_course_units/<course_unit_id>',views.edit_course_units, name='edit_course_units'),
    path('edit_lesson/<lesson_id>',views.edit_lesson, name='edit_lesson'),
    #deleting classes, subjects and lessons
    path('delete_course/<course_id>',views.delete_course, name='delete_course'),
    path('delete_course_units/<course_units_id>',views.delete_course_units, name='delete_course_units'),
    path('delete_lesson/<lesson_id>',views.delete_lesson, name='delete_lesson'),

    #Open Library urls
    path('upload_Freecontent', views.upload_Freecontent, name='upload_Freecontent'),
    path('Freecontent_detail/<int:pk>/', views.Freecontent_detail, name='Freecontent_detail'),
    path('edit_Freecontent/<content_id>',views.edit_Freecontent, name='edit_Freecontent'),
    path('delete_Freecontent/<content_id>',views.delete_Freecontent, name='delete_Freecontent'),
    path('Freecontent_list', views.Freecontent_list, name='Freecontent_list'),
    path('profile_Freelibrary/<int:pk>/', views.profile_Freelibrary, name='profile_Freelibrary'),
    path('profile_Freebooks/<int:pk>/', views.profile_Freebooks, name='profile_Freebooks'),
    #Ebook urls
    path('Freebook_list', views.Freebook_list, name='Freebook_list'),
    path('edit_Freeebook/<ebook_id>',views.edit_Freeebook, name='edit_Freeebook'),
    path('Freebook/<int:pk>/', views.Freebook_details, name='Freebook_details'),
    path('delete_Freeebook/<ebook_id>',views.delete_Freeebook, name='delete_Freeebook'),
    path('Freebook/add/', views.add_Freebook, name='add_Freebook'),
    path('Freebook/<int:book_pk>/add-section/', views.add_Freesection, name='add_Freesection'),
    path('Freesection/<int:section_pk>/add-sub_section/', views.add_Freesub_section, name='add_Freesub_section'),
    path('Freesection/<int:pk>/', views.Freesection_details, name='Freesection_details'),
    #book payments
    
    ]