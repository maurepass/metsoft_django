import json

from .base import *

with open(os.path.join('./METsoft/settings/secrets/', 'development.json'), 'r') as f:
    secrets = json.load(f)

SECRET_KEY = get_secret('SECRET_KEY', secrets),

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