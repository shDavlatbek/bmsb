from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

STATIC_URL = 'https://cdn.e-bmsm.uz/static/'
MEDIA_URL  = 'https://cdn.e-bmsm.uz/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('DB_NAME'),
        'USER': env.str('DB_USER'),
        'PASSWORD': env.str('DB_PASSWORD'),
        'HOST': env.str('DB_HOST'),
        'PORT': env.int('DB_PORT'),
        'ATOMIC_REQUESTS': True,
    }
}

# CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS')
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS')
CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']