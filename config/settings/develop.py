from .base import *
from corsheaders.defaults import default_headers

DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_URL = 'https://cdn-test.e-bmsm.uz/static/'
MEDIA_URL  = 'https://cdn-test.e-bmsm.uz/media/'


CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS')
CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
CORS_ALLOW_HEADERS = list(default_headers) + ["School"]