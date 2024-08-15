from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('about', views.about,name='about'),
    # handling registration of users
    path('register_student',views.register_student,name='register_student'),
    path('register_teacher',views.register_teacher,name='register_teacher'),
    path('register_institution',views.register_institution,name='register_institution'),

    # handling authentication login and logout
    path('login_user',views.login_user,name='login'),
    path('logout_user',views.logout_user,name='logout'),

    # handling user profiles
     path('profiles',views.profiles,name='profiles'),
     path("students",views.students, name='students'),
     path("teachers",views.teachers, name='teachers'),
     path("institutions",views.institutions, name='institutions'),
     path('profile/<int:pk>',views.profile, name='profile'),
     path("update_profile",views.update_profile, name='update_profile')

]



 
 
 