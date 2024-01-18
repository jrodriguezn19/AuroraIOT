from .common import *

print("Using DEV settings")

# Activate or deactivate MQTT operation
MQTT_ACTIVE = True
print(f"MQTT active status is: {MQTT_ACTIVE}")

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

# MQTT Config
'''Important TO-FIX: Not sure why MQTT_SERVER_DEV and MQTT_PORT_DEV are not loading. 
At the moment I'm using the prod variables so I don't have to connect the VPN for DEV'''
MQTT_SERVER = config('MQTT_SERVER_PROD')
MQTT_PORT = config('MQTT_PORT_PROD')
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

def show_toolbar(request):
        return True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}
