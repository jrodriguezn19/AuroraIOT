from .common import *


DEBUG = True

ALLOWED_HOSTS = []

# MQTT Config
MQTT_SERVER_DEV = config('MQTT_SERVER')
MQTT_PORT_DEV = config('MQTT_PORT')
MQTT_USER_DEV = config('MQTT_USER')
MQTT_PASSWORD_DEV = config('MQTT_PASSWORD')

# SQLITE
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": "sqlite3.db",
#     }
# }

# Timescaledb
DATABASES = {
    "default": {
        'ENGINE': 'timescale.db.backends.postgresql',
        "NAME": "auroraiotdb",
        "USER": config('DB_USERNAME_DEV'),
        "PASSWORD": config('DB_PASSWORD_DEV'),
        "HOST": config('DB_HOST_DEV'),
        "PORT": config('DB_PORT_DEV'),
    }
}

# PostgreSQL
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "auroraiotdb",
#         "USER": config('DB_USERNAME_DEV'),
#         "PASSWORD": config('DB_PASSWORD_DEV'),
#         "HOST": config('DB_HOST_DEV'),
#         "PORT": config('DB_PORT_DEV'),
#     }
# }

MQTT_CLIENT_ID = "id-django-mqttclient-development"

print("Using DEV settings")
