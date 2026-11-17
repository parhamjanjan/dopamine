
"""
Django settings for config project.
Django 6.1
"""

from pathlib import Path
import os

import dj_database_url


# ============================================================
# Base
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# Security / Environment
# ============================================================

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-local-development-key-change-me'
)

DEBUG = os.environ.get(
    'DJANGO_DEBUG',
    'False'
).lower() == 'true'


# ============================================================
# Allowed Hosts
# ============================================================

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        'ALLOWED_HOSTS',
        'localhost,127.0.0.1'
    ).split(',')
    if host.strip()
]


# ============================================================
# Application Definition
# ============================================================

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'corsheaders',

    # Local
    'api',
    'accounts',
    'rooms',
    'planner',
    'channels',
    'exams',
    'notes',
]


# ============================================================
# Django REST Framework
# ============================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


# ============================================================
# Middleware
# ============================================================

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ============================================================
# URLs
# ============================================================

ROOT_URLCONF = 'config.urls'


# ============================================================
# Templates
# ============================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ============================================================
# WSGI / ASGI
# ============================================================

WSGI_APPLICATION = 'config.wsgi.application'

ASGI_APPLICATION = 'config.asgi.application'


# ============================================================
# Database
# ============================================================

WASMER_DB_KEYS = [
    'DB_HOST',
    'DB_NAME',
    'DB_USERNAME',
    'DB_PASSWORD',
    'DB_PORT',
]

if all(os.environ.get(key) for key in WASMER_DB_KEYS):

    # Wasmer PostgreSQL

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USERNAME'],
            'PASSWORD': os.environ['DB_PASSWORD'],
            'HOST': os.environ['DB_HOST'],
            'PORT': os.environ['DB_PORT'],

            'CONN_MAX_AGE': 600,
            'CONN_HEALTH_CHECKS': True,

            'OPTIONS': {
                'sslmode': 'require',
            },
        }
    }

elif os.environ.get('DATABASE_URL'):

    # Render PostgreSQL

    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )
    }

else:

    # Local SQLite

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ============================================================
# Password Validation
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]


# ============================================================
# Internationalization
# ============================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# ============================================================
# Static Files
# ============================================================

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}


# ============================================================
# Email
# ============================================================

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}


# ============================================================
# Custom User
# ============================================================

AUTH_USER_MODEL = 'accounts.User'


# ============================================================
# Channels
# ============================================================

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


# ============================================================
# CORS
# ============================================================

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'https://dopamine-st2u.onrender.com',
    'https://dopamine.wasmer.app',
]


# ============================================================
# CSRF
# ============================================================

CSRF_TRUSTED_ORIGINS = [
    'https://dopamine-backend-3vbz.onrender.com',
    'https://dopamine-st2u.onrender.com',
    'https://dopamine.wasmer.app',
]


# ============================================================
# Media
# ============================================================

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# ============================================================
# Backend Public URL
# ============================================================

BACKEND_PUBLIC_URL = os.getenv(
    'BACKEND_PUBLIC_URL',
    'http://127.0.0.1:8000'
)


# ============================================================
# Production Security
# ============================================================

if not DEBUG:

    SECURE_PROXY_SSL_HEADER = (
        'HTTP_X_FORWARDED_PROTO',
        'https',
    )

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 31536000

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_HSTS_PRELOAD = True


# ============================================================
# Default Primary Key
# ============================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
