from .common import *


DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "sqlite3.db",
    }
}

MQTT_CLIENT_ID = "id-django-mqttclient-development"

print("Using DEV settings")