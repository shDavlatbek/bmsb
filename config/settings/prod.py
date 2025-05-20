from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': env.str('DB_NAME'),
#         'USER': env.str('DB_USER'),
#         'PASSWORD': env.str('DB_PASSWORD'),
#         'HOST': env.str('DB_HOST'),
#         'PORT': env.int('DB_PORT'),
#         'ATOMIC_REQUESTS': True,
#     }
# }