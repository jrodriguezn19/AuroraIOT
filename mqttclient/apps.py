from django.apps import AppConfig
from django.conf import settings

class MqttclientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mqttclient'

    def ready(self):
        from mqttclient import mqtt      
        if settings.MQTT_ACTIVE:
            mqtt.client.loop_start()