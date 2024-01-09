from .common import *


DEBUG = True

ALLOWED_HOSTS = []

# MQTT Config
MQTT_SERVER = config('MQTT_SERVER_DEV')
MQTT_PORT = config('MQTT_PORT_DEV', cast=int)
MQTT_CLIENT_ID = "id-django-mqttclient-development"
MQTT_USER = config('MQTT_USER_DEV')
MQTT_PASSWORD = config('MQTT_PASSWORD_DEV')

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



print("Using DEV settings")
