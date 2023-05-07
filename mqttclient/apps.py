from django.apps import AppConfig


class MqttclientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mqttclient'

    def ready(self):
        from mqttclient import mqtt      
        mqtt.client.loop_start()