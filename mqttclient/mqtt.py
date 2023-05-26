import paho.mqtt.client as mqtt
from sensors.models import Data, Sensor
import json
from decouple import config
from AuroraIOT.settings import MQTT_ACTIVE

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
if MQTT_ACTIVE:
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.username_pw_set(config('MQTT_USER'), config('MQTT_PASSWORD'))
    client.connect(host=config('MQTT_SERVER'), port=config('MQTT_PORT', cast=int), keepalive=config('MQTT_KEEPALIVE', cast=int))


