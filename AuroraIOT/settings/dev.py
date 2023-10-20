from .common import *


DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "auroraiotdb",
        "USER": config('DB_USERNAME_DEV'),
        "PASSWORD": config('DB_PASSWORD_DEV'),
        "HOST": config('DB_HOST_DEV'),
        "PORT": config('DB_PORT_DEV'),
    }
}

MQTT_CLIENT_ID = "id-django-mqttclient-development"

print("Using DEV settings")