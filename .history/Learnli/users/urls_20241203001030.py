from django.urls import path
from . import views
#from django.contrib.auth import views as auth_views

  

urlpatterns = [
    path('', views.home,name='home'),
    path('copyright', views.copyright,name='copyright'),
    path('about', views.about,name='about'),
    # handling registration of users
    path('register_student',views.register_student,name='register_student'),
    path('register_teacher',views.register_teacher,name='register_teacher'),
    path('register_institution',views.register_institution,name='register_institution'),

    # handling authentication login and logout
    path('login_user',views.login_user,name='login'),
    path('logout_user',views.logout_user,name='logout'),
    path('subscribe', views.subscription_page, name='subscription_page'),  # Subscription page
    path('payment_success',views.payment_success, name='payment_success'),  # Payment success page
    
    

    # handling user       
     path('profiles',views.profiles,name='profiles'),
     path("students",views.students, name='students'),
     path("teachers",views.teachers, name='teachers'),
     path("institutions",views.institutions, name='institutions'),
     path('profile/<int:pk>',views.profile, name='profile'),
     path("update_profile",views.update_profile, name='update_profile'),

   
    
      # Password reset views
       #path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
       #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
       #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
       #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]



 
 
 