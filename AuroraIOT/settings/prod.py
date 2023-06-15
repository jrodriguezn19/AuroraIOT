import os
from .common import *


DEBUG = False

ALLOWED_HOSTS = ['*']

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": "sqlite3.db",
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "auroraiotdb",
        "USER": config('DB_USERNAME'),
        "PASSWORD": config('DB_PASSWORD'),
        "HOST": config('DB_HOST'),
        "PORT": config('DB_PORT'),
    }
}

def show_toolbar(request):
        return True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}

# SECURE_CROSS_ORIGIN_OPENER_POLICY = None

# import mimetypes
# mimetypes.add_type("text/css", ".css", True)

print("Using PROD settings")