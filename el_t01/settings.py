#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os

from el_t01.env import ENV_DEBUG
from el_t01.env import DATABASE_HOST, DATABASE_PORT, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD
# from el_t01.env import ENV_EMAIL_HOST, ENV_EMAIL_HOST_USER, ENV_EMAIL_HOST_USER_NAME, \
#     ENV_EMAIL_HOST_PASSWORD, ENV_EMAIL_PORT, ENV_EMAIL_USE_TLS, ENV_DEFAULT_FROM_EMAIL, ENV_LOGO_FOR_MAIL, \
#     ENV_EMAIL_SERVICE_NAME


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 't2-vv0tw+s-^$0mx)$6=%-h!x8c&x&#7@0vbum)^ms8@(8w@w('
DEFAULT_CHARSET = 'utf-8'
DEBUG = ENV_DEBUG

SESSION_EXPIRE_AT_BROWSER_CLOSE = None

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

ALLOWED_HOSTS = ['*']

CSRF_FAILURE_VIEW = 'el_t01_app.views_main.error403'

INSTALLED_APPS = [
    'i18next',
    "django_admin_index",
    "ordered_model",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'el_t01_app',
    'django_crontab',
    'el_t0001_app',
    'el_t0002_app',
    'el_t0003_app',
    'el_t0004_app',
    'el_t0005_app',
]

CRONJOBS = [
    ('*/5 * * * *', 'el_t01_app.service.periodic_tasks.group_sms', '>> /var/log/sod/cron/cron_el_t01.log '),
]
CRONTAB_DJANGO_PROJECT_NAME = 'el_t01'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'el_t01.urls'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATE_DIRS,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'el_t01.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
    },
}

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

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
# LANGUAGE_CODE = 'ru-RU'
# LANGUAGE_CODE = 'en-EN'
# LANGUAGE_CODE = 'en-us'
# LANGUAGE_CODE = 'en'
LANGUAGE_CODE = 'he'

TIME_ZONE = 'Europe/Kiev'
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'el_t01_app', 'static')

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = (
    ('ru', 'Russian'),
    ('ua', 'Ukrainian'),
    ('en', 'English'),
    ('he', 'Hebrew'),
    ('ar', 'Arabic'),
    ('pl', 'Poland'),
)

DATA_UPLOAD_MAX_MEMORY_SIZE = 10000000
# DOMAIN = ENV_DOMAIN
# CONFIRMATION_REGISTRATION = ENV_CONFIRMATION_REGISTRATION

# LOGIN_URL = '/userlogin/'
# LOGIN_REDIRECT_URL = '/cab-balance/'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

ASGI_APPLICATION = "el_t01.asgi.application"
