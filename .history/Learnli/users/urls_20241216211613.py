from django.urls import path
from . import views
#from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home,name='home'),
    path('copyright', views.copyright,name='copyright'),
    # content moderation guidelines
    path('course_guide', views.course_guide,name='course_guide'),
    path('blogs_guide', views.blogs_guide,name='blogs_guide'),
    path('lessons_guide', views.lessons_guide,name='lessons_guide'),
    path('ebook_guide', views.ebook_guide,name='ebook_guide'),
    path('content_guide', views.content_guide,name='content_guide'), 

    path('about', views.about,name='about'),
    path('FAQs', views.FAQs,name='FAQs'),
    # handling registration of users
    path('register_student',views.register_student,name='register_student'),
    path('register_teacher',views.register_teacher,name='register_teacher'),
    path('register_institution',views.register_institution,name='register_institution'),

    # handling authentication login and logout
    path('login_user',views.login_user,name='login'),
    path('logout_user',views.logout_user,name='logout'),
    path('subscribe', views.subscription_page, name='subscription_page'),  # Subscription page
    path('payment_success',views.payment_success, name='payment_success'),  # Payment success page
    # Assistant
    path('chat', views.chat, name='chat'),
    

    # handling user       
     path('profiles',views.profiles,name='profiles'),
     path("students",views.students, name='students'),
     path("teachers",views.teachers, name='teachers'),
     path("institutions",views.institutions, name='institutions'),
     path('profile/<int:pk>',views.profile, name='profile'),
     path("update_profile",views.update_profile, name='update_profile'),
     #content moderaqtion
    path('moderation_tool', views.moderation_tool,name='moderation_tool'),
    path('reported_blogs', views.reported_blogs,name='reported_blogs'),
    path('reported_ebooks', views.reported_ebooks,name='reported_ebooks'),
    path('reported_content', views.reported_content,name='reported_content'),
    path('reported_courses', views.reported_courses,name='reported_courses'), 
    path('reported_lessons', views.reported_lessons,name='reported_lessons'), 


    path('report_content/<int:content_type_id>/<int:object_id>/',views.report_content, name='report_content'),
    path('approve_flag/<flag_id>',views.approve_flag, name='approve_flag'),
    path('reject_flag/<flag_id>',views.reject_flag, name='reject_flag'),
    path('escaleting_flag/<flag_id>',views.escaleting_flag, name='escaleting_flag'),
    
 

]
 