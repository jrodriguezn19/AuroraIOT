from .common import *

logger.info("Using PROD settings")

# Activate or deactivate MQTT operation
MQTT_ACTIVE = True
logger.info(f"MQTT active status is: {MQTT_ACTIVE}")

DEBUG = False

#CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8000",
#     "http://127.0.0.1:8000",
# ]

# ALLOWED_HOSTS = ['.georgedeveloper.com']
ALLOWED_HOSTS = ['*']

# MQTT Config
MQTT_SERVER = config('MQTT_SERVER_PROD')
MQTT_PORT = config('MQTT_PORT_PROD')
MQTT_CLIENT_ID = "id-mqttclient-django-production"
MQTT_USER = config('MQTT_USER_PROD')
MQTT_PASSWORD = config('MQTT_PASSWORD_PROD')
MQTT_KEEPALIVE = 60

# Timescaledb
DATABASES = {
    "default": {
        'ENGINE': 'timescale.db.backends.postgresql',
        "NAME": "auroraiotdb",
        "USER": config('DB_USERNAME_PROD'),
        "PASSWORD": config('DB_PASSWORD_PROD'),
        "HOST": config('DB_HOST_PROD'),
        "PORT": config('DB_PORT_PROD'),
    }
}

# PostgreSQL
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "auroraiotdb",
#         "USER": config('DB_USERNAME_PROD'),
#         "PASSWORD": config('DB_PASSWORD_PROD'),
#         "HOST": config('DB_HOST_PROD'),
#         "PORT": config('DB_PORT_PROD'),
#     }
# }

# def show_toolbar(request):
#         return False

# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TOOLBAR_CALLBACK': show_toolbar,
# }

