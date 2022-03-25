"""
Django settings for WebServices project.

Based on 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import posixpath

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dbaea3ac-db35-4a50-9a85-664a9b0901f3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '10.19.1.223', '10.19.1.240'] # Ref: https://docs.djangoproject.com/en/3.0/ref/settings/#allowed-hosts

# Application references
# https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-INSTALLED_APPS
INSTALLED_APPS = [
    # My apps:
    'home',
    'accounts',
    'dashboard',
    'database_api',
    # Other modules:
    'channels',
    # Django apps:
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Middleware framework
# https://docs.djangoproject.com/en/2.1/topics/http/middleware/
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'WebServices.urls'

# Template configuration
# https://docs.djangoproject.com/en/2.1/topics/templates/
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['WebServices/templates'],
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

WSGI_APPLICATION = 'WebServices.wsgi.application'

# Setting Channels:
# Needs Docker to start redis server: https://hub.docker.com/editions/community/docker-ce-desktop-windows
# After installing (and at each OS reboot), open terminal and run: docker run -p 6379:6379 -d redis:2.8
# Ref: https://channels.readthedocs.io/en/latest/tutorial/part_2.html
# Alternative to Docker (?): https://realpython.com/getting-started-with-django-channels/
ASGI_APPLICATION = 'WebServices.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# Database
'''
Refs:
https://stackoverflow.com/questions/61840428/connecting-django-to-microsoft-sql-database
https://pypi.org/project/django-mssql-backend/
Download Microsoft® ODBC Driver 17 for SQL Server: https://www.microsoft.com/en-us/download/confirmation.aspx?id=56567
'''
DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'HOST': '.\SQLEXPRESS',
        'PORT': '',
        'NAME': 'GA',
        #'USER': 'USER',
        #'PASSWORD': 'PASSWORD',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'unicode_results': True,
        },
    },
}

# SRV02 - Não conectando 2021-07: pyodbc.InterfaceError: ('IM002', [IM002] [Microsoft][ODBC Driver Manager] Data source name not found and no default driver specified (0) (SQLDriverCionnect)')
#DATABASES = {
#    'default': {
#        'ENGINE': 'sql_server.pyodbc',
#        'HOST': 'localhost\innovix',
#        'PORT': '',
#        'NAME': 'GA',
#        'USER': 'adm.ga',
#        'PASSWORD': 'GA@CNI@GA1000',
#        'OPTIONS': {
#            'driver': 'ODBC Driver 17 for SQL Server',
#            'unicode_results': True,
#        },
#    },
#}

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
STATICFILES_DIRS = [
    posixpath.join(*(BASE_DIR.split(os.path.sep) + ['WebServices/static']))
    ]
STATIC_URL = '/static/'
STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))
