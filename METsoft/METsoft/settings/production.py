import json

from .base import *



with open(os.path.join('/var/www/metsoft_django/METsoft/METsoft/settings/secrets/', 'production.json'), 'r') as f:
    secrets = json.load(f)

SECRET_KEY = get_secret('SECRET_KEY', secrets),

ALLOWED_HOSTS = ["192.168.1.127", 'localhost']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

STATIC_ROOT = "/var/www/metsoft_django/METsoft/static"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_secret('DEFAULT_DB_NAME', secrets),
        'HOST': get_secret('DEFAULT_DB_HOST', secrets),
        'USER': get_secret('DEFAULT_DB_USER', secrets),
        'PASSWORD': get_secret('DEFAULT_DB_PASSWORD', secrets),
        'PORT': 3306
    },
    'kokila': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_secret('KOKILA_DB_NAME', secrets),
        'HOST': get_secret('KOKILA_DB_HOST', secrets),
        'USER': get_secret('KOKILA_DB_USER', secrets),
        'PASSWORD': get_secret('KOKILA_DB_PASSWORD', secrets),
        'PORT': 3306
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = get_secret('EMAIL_HOST', secrets)
EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER', secrets)
EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD', secrets)
EMAIL_PORT = 587