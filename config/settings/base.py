from pathlib import Path
from decouple import config
from .ckeditor import *
from .jazzmin import *
from .email_data import *
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent.parent

if config('PROD', cast=bool):
    from .prod import *
else: 
    from .dev import *

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG')


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'phonenumber_field',
    'phonenumbers',
    'rest_framework',
    'djoser',
    'django_ckeditor_5',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'corsheaders',

    'apps.generals',
    'apps.users',
    'apps.packages',
    'apps.settings',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


REST_FRAMEWORK = {
    # YOUR SETTINGS
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication' ,
    ],
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'CARGO',
    'DESCRIPTION': 'CARGO description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
}


SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=1000000),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=6000000),
}

DJOSER = {
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SEND_ACTIVATION_EMAIL': False,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'TOKEN_MODEL': None,
    'ACTIVATION_URL': 'auth/verify/{uid}/{token}/',
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'users.User'

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True
USE_L10N = True

USE_TZ = True

STATIC_URL = 'back_static/'
STATIC_ROOT = BASE_DIR / 'back_static'
STATICFILES_DIRS = [BASE_DIR / 'locale_static',]

if config('DOMAIN_NAME', default=''):
    MEDIA_URL = f'https://{config("DOMAIN_NAME")}/back_media/'
    MEDIA_ROOT = BASE_DIR / 'back_media'
else:
    MEDIA_URL = 'back_media/'
    MEDIA_ROOT = BASE_DIR / 'back_media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True


USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]
