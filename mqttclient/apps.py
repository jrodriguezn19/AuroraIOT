from django.apps import AppConfig
from AuroraIOT.settings import MQTT_ACTIVE


class MqttclientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mqttclient'

    def ready(self):
        from mqttclient import mqtt      
        if MQTT_ACTIVE:
            mqtt.client.loop_start()