"""
Django settings for django_app project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

import environ

env = environ.Env()
environ.Env.read_env()  # reading .env file

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# Application definition
DJANGO_CORE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "health_check",  # required
    "health_check.db",  # stock Django health checkers
    # "health_check.cache",
    # "health_check.storage",
    "health_check.contrib.migrations",
    # "health_check.contrib.celery",  # requires celery
    # "health_check.contrib.celery_ping",  # requires celery
    # "health_check.contrib.psutil",  # disk and memory utilization; requires psutil
    # "health_check.contrib.s3boto3_storage",  # requires boto3 and S3BotoStorage backend
    # "health_check.contrib.rabbitmq",  # requires RabbitMQ broker
    # "health_check.contrib.redis",  # requires Redis broker
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "django_filters",
    "silk",
    "djstripe",
    "django_celery_beat",
]

LOCAL_APPS = ["djlodging.domain.lodgings", "djlodging.domain.bookings", "djlodging.domain.users"]

INSTALLED_APPS = DJANGO_CORE_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "silk.middleware.SilkyMiddleware",
]

ROOT_URLCONF = "djlodging.django_app.django_core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "djlodging.django_app.django_core.wsgi.application"

# https://docs.djangoproject.com/en/4.0/ref/settings/#csrf-trusted-origins
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": env.str("POSTGRES_HOST"),
        "PORT": env.str("POSTGRES_PORT", default="5432"),
        "ATOMIC_REQUESTS": True,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL)

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGE_SIZE": 1,
    "EXCEPTION_HANDLER": "djlodging.api.exception_handlers.custom_exception_handler",  # noqa pylint: disable=line-too-long
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "dj-lodging API",
    "DESCRIPTION": "Django powered lodging reservation application",
    "VERSION": "1.0.0",
    "SCHEMA_PATH_PREFIX": "/api/",
    "SCHEMA_COERCE_PATH_PK_SUFFIX": True,
    "COMPONENT_SPLIT_REQUEST": True,
    "SERVE_INCLUDE_SCHEMA": False,
}

SECURITY_TOKEN_LIFE_TIME_IN_HOURS = env.int("SECURITY_TOKEN_LIFE_TIME_IN_HOURS", default=2)

# EMAIL SETTINGS
EMAIL_BACKEND = env.str(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", default="example@example.com")
EMAIL_PROVIDER = "djlodging.infrastructure.providers.email.SendgridEmailProvider"
EMAIL_PROVIDER_SETTINGS = {
    "API_KEY": env.str("EMAIL_PROVIDER_API_KEY", default="SET_YOUR_API_KEY"),
    "CONFIRMATION_LINK_TEMPLATE_ID": "d-118c70b3aa884c74af9d3c14403aa4f5",
    "CHANGE_PASSWORD_LINK_TEMPLATE_ID": "d-788fb445f4b24970abf871901cf43d96",
    "CHANGE_EMAIL_LINK_TEMPLATE_ID": "d-27e74abd0a49487ca6bd59cd95081d27",
    "BOOKING_CONFIRMATION_EMAIL_FOR_USER_TEMPLATE_ID": "d-07202cd50655498587d59a73929aea24",
    "BOOKING_CONFIRMATION_EMAIL_FOR_OWNER_TEMPLATE_ID": "d-ca813fa9a96542dc8c6fd3345485e737",
    # "BOOKING_CANCELLATION_EMAIL_FOR_USER_TEMPLATE_ID":,
    # "BOOKING_CANCELLATION_EMAIL_FOR_OWNER_TEMPLATE_ID":
}
DOMAIN = "https://dj-lodging.com"

# CELERY SETTINGS
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_BEAT_SCHEDULE = {
    "delete_users_with_unfinished_registration": {
        "task": "djlodging.infrastructure.jobs.celery_tasks.delete_users_with_unfinished_registration",  # noqa
        "schedule": timedelta(
            hours=env.int(
                "CELERY_BEAT_DELETE_USERS_WITH_UNFINISHED_REGISTRATION_INTERVAL", default=24
            )
        ),
    },
}

# PAYMENT SETTINGS
PAYMENT_PROVIDER = "djlodging.infrastructure.providers.payments.StripePaymentProvider"
STRIPE_LIVE_SECRET_KEY = env.str("STRIPE_LIVE_SECRET_KEY", "<your secret key>")
STRIPE_TEST_SECRET_KEY = env.str("STRIPE_TEST_SECRET_KEY", "<your secret key>")
STRIPE_API_KEY = STRIPE_TEST_SECRET_KEY if DEBUG else STRIPE_LIVE_SECRET_KEY
STRIPE_LIVE_MODE = False  # Change to True in production
DJSTRIPE_WEBHOOK_SECRET = env.str(
    "DJSTRIPE_WEBHOOK_SECRET"
)  # Get it from the section in the Stripe dashboard where you added the webhook endpoint
DJSTRIPE_USE_NATIVE_JSONFIELD = True  # We recommend setting to True for new installations
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"
BOOKING_PAYMENT_EXPIRATION_TIME_IN_MINUTES = env.int(
    "BOOKING_PAYMENT_EXPIRATION_TIME_IN_MINUTES", default=15
)
