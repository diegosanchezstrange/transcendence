"""
Django settings for front project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from environ import Env
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-82(6is-9=axy572@fz*r7d_zqmy5cyhf4lfw7j85b5#@m#jdlf'
SECRET_KEY = os.getenv('JWT_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv('DEBUG'))

ALLOWED_HOSTS = [ "*" ]

APPEND_SLASH = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'game.apps.GameConfig',
    'front',
    'users',
    'login.apps.LoginConfig',
    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'front.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'front.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

env = Env()

Env.read_env()

# 42 API
LOGIN_42 = os.getenv('LOGIN_42')
LOGIN_42_URL = os.getenv('LOGIN_42_URL')

LOGIN_42_REDIRECT_URI = os.getenv('REDIRECT_URI')
LOGIN_42_CLIENT = os.getenv('LOGIN_42_CLIENT')
LOGIN_42_SECRET = os.getenv('LOGIN_42_SECRET')
# CLIENT_ID = env('CLIENT_ID')
# SECRET_KEY = env('SECRET_KEY')

# Microservices URL's
LOGIN_SERVICE_HOST = os.getenv('LOGIN_SERVICE_HOST')
LOGIN_SERVICE_HOST_INTERNAL = os.getenv('LOGIN_SERVICE_HOST_INTERNAL')

USERS_SERVICE_HOST = os.getenv('USERS_SERVICE_HOST')
USERS_SERVICE_HOST_INTERNAL = os.getenv('USERS_SERVICE_HOST_INTERNAL')

USER_URL = os.getenv('USERS_SERVICE_HOST')
NOTIFICATIONS_SERVICE_HOST = os.getenv('NOTIFICATIONS_SERVICE_HOST')
NOTIFICATIONS_SOCKETS_HOST = os.getenv('NOTIFICATIONS_SOCKETS_HOST')

GAME_SOCKETS_HOST = os.getenv('GAME_SOCKETS_HOST')

# GAME_URL = env('GAME_URL')
# MATCH_URL = env('MATCH_URL')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USERNAME'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOSTNAME'),
        'PORT': os.getenv('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/front/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = '/static/front'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
