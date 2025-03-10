"""Learnli URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from two_factor.urls import urlpatterns as tf_urls



urlpatterns = [

    path('admin/', admin.site.urls),
    path('',include('users.urls')),
    path('',include('Works.urls')),
    path('',include('Messages.urls')),
    path('',include('Examination.urls')),
    path('', include('blogs.urls')),
    path('', include('free.urls')),
    path('', include('my_library.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include(tf_urls)),
    
   # path('',include('django.contrib.auth.urls')),
    #path('',include('two_factor.urls','two_factor')),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
