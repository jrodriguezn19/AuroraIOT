import paho.mqtt.client as mqtt
from sensors.models import Data, Sensor
import json
from decouple import config
from AuroraIOT.settings.dev import MQTT_ACTIVE
import datetime
import time


#rc = returned code
# Connection Return Codes
# 0: Connection successful
# 1: Connection refused – incorrect protocol version
# 2: Connection refused – invalid client identifier
# 3: Connection refused – server unavailable
# 4: Connection refused – bad username or password
# 5: Connection refused – not authorised
# 6-255: Currently unused.


#callback function
def on_connect(mqtt_client, userdata, flags, rc):
    print("MQTT: Connected with result code " + str(rc))
    if rc == 0:
        mqtt_client.connected_flag=True
        print('MQTT: Connected successfully, returned code=', rc)
        mqtt_client.subscribe('auroraiot/energy')
    else:
        print('MQTT: Bad connection, returned code=', rc)
        mqtt_client.bad_connection_flag=True


#callback function
FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

def on_disconnect(mqtt_client, userdata, rc):
    #logging.info("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        #logging.info("Reconnecting in %d seconds...", reconnect_delay)
        print("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            mqtt_client.reconnect()
            # logging.info("Reconnected successfully!")
            print("Reconnected successfully!")
            return
        except Exception as err:
            # logging.error("%s. Reconnect failed. Retrying...", err)
            print("%s. Reconnect failed. Retrying...", err)
        
        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    # logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)

# def on_disconnect(mqtt_client, userdata, rc):
#     #logging.info("disconnecting reason  "  +str(rc))
#     mqtt_client.connected_flag=False
#     mqtt_client.disconnect_flag=True
#     #mqtt_client.loop_stop(force=False) # removed instruction so it will try to reconnect automatically
#     if rc != 0:
#         print("MQTT: Unexpected disconnection, returned code=", rc)
#     else:
#         print("MQTT: Disconnected, returned code=", rc)


#callback function
def on_message(mqtt_client, userdata, msg):
    string_payload = msg.payload.decode('utf8').replace("'", '"')
    try:
        json_payload = json.loads(string_payload)
        Data.objects.create(sensor_id=Sensor(
            id=json_payload["sensor_id"]), data=json_payload["data"])
        print(datetime.datetime.now())
        print(f'Topic: {msg.topic} \n Payload: {json_payload}\n')
    except ValueError as err:
        print("Json data recevied from MQTT not valid or empty - Error:", err)
        print("Erroneous payload received was: ", string_payload)


client = mqtt.Client(client_id="id-django-mqttclient")
if MQTT_ACTIVE:
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.username_pw_set(config('MQTT_USER'), config('MQTT_PASSWORD'))
    client.connected_flag = False
    client.bad_connection_flag = False
    try:
        client.connect(
            host=config('MQTT_SERVER'), 
            port=config('MQTT_PORT', cast=int), 
            keepalive=60)
    except:
        print("MQTT client.connect() failed")
        exit(1)

    # not sure if this loops is good
    # while not client.connected_flag and not client.bad_connection_flag: #wait in loop
    #     print("In wait loop")
    #     time.sleep(1)
    #     if client.bad_connection_flag:
    #         client.loop_stop()    #Stop loop
    #         exit(1)
