import os
from django.apps import AppConfig
from django.conf import settings


class MqttclientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mqttclient'

    def ready(self):
        # Django's dev server (runserver) calls ready() twice: once in the
        # parent process and once in the auto-reloader child (RUN_MAIN=true).
        # Only start MQTT in the child so there is exactly one client.
        # In Gunicorn/production RUN_MAIN is not set and ready() runs once.
        is_dev_server = os.environ.get('RUN_MAIN') is not None
        if is_dev_server and os.environ.get('RUN_MAIN') != 'true':
            return

        if settings.MQTT_ACTIVE:
            from mqttclient import mqtt
            mqtt.start()
