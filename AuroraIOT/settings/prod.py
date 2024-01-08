from .common import *


DEBUG = False

ALLOWED_HOSTS = ['*']

# MQTT Config
MQTT_SERVER_PROD = config('MQTT_SERVER')
MQTT_PORT_PROD = config('MQTT_PORT')
MQTT_USER_PROD = config('MQTT_USER')
MQTT_PASSWORD_PROD = config('MQTT_PASSWORD')

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
        "USER": config('DB_USERNAME_PROD'),
        "PASSWORD": config('DB_PASSWORD_PROD'),
        "HOST": config('DB_HOST_PROD'),
        "PORT": config('DB_PORT_PROD'),
    }
}

def show_toolbar(request):
        return True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}

MQTT_CLIENT_ID = "id-django-mqttclient-production"


print("Using PROD settings")