import paho.mqtt.client as mqtt
from django.conf import settings


def on_connect(mqtt_client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe('auroraiot/energy')
    else:
        print('Bad connection. Code:', rc)


def on_disconnect(mqtt_client, userdata, rc):
    mqtt_client.loop_stop(force=False)
    if rc != 0:
        print("Unexpected disconnection.")
    else:
        print("Disconnected")


def on_message(mqtt_client, userdata, msg):
    print(f'Topic: {msg.topic} \n Payload: {msg.payload}')
    print("\n")


client = mqtt.Client(client_id="django-mqttclient")
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(host=settings.MQTT_SERVER, port=settings.MQTT_PORT, keepalive=settings.MQTT_KEEPALIVE)
