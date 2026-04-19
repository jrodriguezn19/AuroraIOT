import fcntl
import os
import sys
from django.apps import AppConfig
from django.conf import settings

_mqtt_lock_fd = None  # held for the worker's lifetime to keep the lock active


class MqttclientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mqttclient'

    def ready(self):
        if not settings.MQTT_ACTIVE:
            return

        # Django dev server spawns a reloader parent + child; only the child
        # (RUN_MAIN=true) should start MQTT to avoid two instances.
        if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') != 'true':
            return

        # Gunicorn spawns multiple workers and each calls ready(). Use a
        # non-blocking exclusive file lock so only the first worker starts
        # MQTT. If that worker dies, Gunicorn restarts it and it re-acquires.
        global _mqtt_lock_fd
        try:
            lock_fd = open('/tmp/auroraiot_mqtt.lock', 'w')
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            _mqtt_lock_fd = lock_fd
        except (IOError, OSError):
            return  # another worker already holds the lock

        from mqttclient import mqtt
        mqtt.start()
