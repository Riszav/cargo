from .base import BASE_DIR

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1/", "http://127.0.0.1:8000", "http://127.0.0.1:80"]

