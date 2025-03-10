"""
Django settings for Learnli project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
from pathlib import Path
import os
import dj_database_url  # To handle the database URL from Railway
from decouple import config
import dj_database_url
 
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('YOUR_DJANDO_SECRET_KEY'),

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('YOUR_DEBUG')

ALLOWED_HOSTS = ['*'] 
#csrf_token configuration to adid ngrok
CSRF_TRUSTED_ORIGINS = [ 'YOUR_URLS/SITES']

AUTH_USER_MODEL ='users.user_Profile'

 
# Application definition

INSTALLED_APPS = [
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_email',
     'two_factor',
     'two_factor.plugins.phonenumber',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'Works',
    'Messages',
    'Examination',
    'blogs',
    'free',
    'my_library',
    'django.contrib.humanize',
    'ckeditor',
    'ckeditor_uploader',
    'crispy_forms',
    'phonenumber_field',
    'whitenoise.runserver_nostatic',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'Learnli.middleware.CheckSubscriptionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  
   
]


# Gmail's SMTP server CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'learnlI@gmail.com'  # Replace with your email
EMAIL_HOST_PASSWORD = ' PASS_WORD'  # Replace with your email passwor
DEFAULT_FROM_EMAIL = 'webmaster@example.com'


# Flutterwave configuration
 
#FLWSECK_TESTe38b7f33b30d
FLUTTERWAVE_PUBLIC_KEY = os.getenv('FLUTTERWAVE_PUBLIC_KEY') #configure thyes secrete keys in your .env files
FLUTTERWAVE_SECRET_KEY = os.getenv('FLUTTERWAVE_SECRET_KEY')
# Flutterwave Secret Key
#openai api key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")#configure thyes secrete keys in your .env files

# Twilio SMS Configuration (Optional)
TWILIO_ACCOUNT_SID = 'your_twilio_account_sid'
TWILIO_AUTH_TOKEN = 'your_twilio_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'

# Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'




# Crispy forms configuration
CRISPY_TEMPLATE_PACK = 'bootstrap4'


# Session settings 
'''

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600  # 1 hour


'''

# Timezone settings
USE_TZ = True
TIME_ZONE = 'Africa/Kampala'



SITE_ID = 1

ROOT_URLCONF = 'Learnli.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR,'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Learnli.wsgi.application'
 

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
 
 
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''
# configure your database
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')  # Load the DATABASE_URL from .env
    )
}

  


 



# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
 

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

#White noise static stuff
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT =  os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CKEDITOR_UPLOAD_PATH = "/uploads/"
CKEDITOR_BASE_PATH = "/static/ckeditor/ckeditor/"
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
        'default': {
            'toolbar': 'full',
            'extraPlugins': ','.join([
                'mathjax',
            ]),
            'mathJaxLib': 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML',
        },
    }



LOGIN_URL = 'login'
LOGIN_REDIRECT_URL ='/'


#LOGIN_URL = 'login'  # The URL name for the login view
LOGOUT_URL = 'logout'  # The URL name for the logout view
LOGIN_REDIRECT_URL = '/'  # The default URL to redirect to after login
#LOGOUT_REDIRECT_URL = '/'  # The URL to redirect to after logout

'''
#Log errors in production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django_errors.log',  # Change this path if needed
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

'''


