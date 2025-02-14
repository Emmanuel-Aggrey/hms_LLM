import os
from datetime import timedelta
from pathlib import Path


from dotenv import dotenv_values

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


config = {
    # load sensitive variables
    **os.environ,  # override loaded values with environment variables
    **dotenv_values(".env"),
}


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.get("DEBUG") == "True"
TEST_DEBUG = False

APP_DOMAIN = config.get(
    "DOMAIN",
)


ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    *config.get("ALLOWED_HOSTS", "").split(","),
]


INSTALLED_APPS = [

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    # Third party apps

    "rest_framework",
    "drf_yasg",
    "corsheaders",
    "rest_framework_simplejwt",
    "django_filters",
    'django_celery_beat',
    'django_extensions',

    # Local apps
    "accounts",
    "api",
    "booking",
    "doctorsnote",
    "actionable_steps",



]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "core.urls"
AUTH_USER_MODEL = "accounts.User"

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

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config.get("DATABASE_NAME"),
        "USER": config.get("DATABASE_USER"),
        "PASSWORD": config.get("DATABASE_PASSWORD"),
        "HOST": config.get("DATABASE_HOST"),
        "PORT": config.get("DATABASE_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
MEDIA_ROOT_NAME = "media"
STATIC_LOCATION = "static/"


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


FILEFIELD_MAX_LENGTH = int(config.get("FILEFIELD_MAX_LENGTH", 100000))


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    "https://127.0.0.1" "http://*.127.0.0.1",
    "http://localhost",
    config.get("FRONTEND_URL", ""),
    *config.get("CSRF_TRUSTED_ORIGINS", "http://localhost").split(","),
]


# Rest Frame work
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],




    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": int(config.get("PAGE_SIZE", 30)),
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],



}
# swagger
# https://drf-yasg.readthedocs.io/en/stable/readme.html
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"},
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=90),
    "AUTH_HEADER_TYPES": ("Bearer",),
}


TEST_RUNNER = "testing.test_runner.CustomTestRunner"

# ipython config for remote shell
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
NOTEBOOK_ARGUMENTS = [
    "--allow-root",
    "--port=8888",
    "--ip=0.0.0.0",
    "--NotebookApp.token=''",
    "--NotebookApp.password=''",
]


if not DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    }


INTERNAL_IPS = [
    "localhost",
    "127.0.0.1",
]


LLM_API_KEY = config.get('LLM_API_KEY')


CELERY_BROKER_URL = config.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = config.get('CELERY_RESULT_BACKEND')
CELERY_CACHE_BACKEND = 'default'


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config.get("EMAIL_HOST")
EMAIL_PORT = config.get("EMAIL_PORT")
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = config.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
