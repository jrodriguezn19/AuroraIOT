import paho.mqtt.client as mqtt
from django.conf import settings
from .models import Data, Sensor
import json

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
    string_payload = msg.payload.decode('utf8').replace("'", '"')
    json_payload = json.loads(string_payload)
    Data.objects.create(sensor_id=Sensor(id=json_payload["sensor_id"]), data=json_payload["data"])
    print(f'Topic: {msg.topic} \n Payload: {json_payload}\n')

client = mqtt.Client(client_id="django-mqttclient")
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(host=settings.MQTT_SERVER, port=settings.MQTT_PORT, keepalive=settings.MQTT_KEEPALIVE)
