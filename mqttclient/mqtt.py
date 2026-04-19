import json
import time
import logging

import paho.mqtt.client as mqtt
from django.conf import settings

from sensors.models import Sensor, Data_PZEM004t
from mqttclient.models import Data_Received

logger = logging.getLogger(__name__)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        logger.info(f'MQTT: Connected successfully, returned code = {rc}')
        client.subscribe('auroraiot/energy', qos=1)
    else:
        logger.error(f'MQTT: Bad connection, returned code = {rc}')
        client.bad_connection_flag = True


FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60


def on_disconnect(client, userdata, rc):
    logger.warning(f"MQTT: Disconnected with result code {rc}")
    client.connected_flag = False
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logger.info(f"MQTT: Reconnecting in {reconnect_delay} seconds...")
        time.sleep(reconnect_delay)
        try:
            client.reconnect()
            logger.info("MQTT: Reconnected successfully!")
            return
        except Exception as err:
            logger.error(f"MQTT: {err}. Reconnect failed. Retrying...")
        reconnect_delay = min(reconnect_delay * RECONNECT_RATE, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logger.error(f"MQTT: Reconnect failed after {MAX_RECONNECT_COUNT} attempts.")


def on_message(mqtt_client, userdata, msg):
    try:
        string_payload = msg.payload.decode('utf8').replace("'", '"')

        if string_payload == "ESP32 Connected to MQTT Broker":
            return

        json_payload = json.loads(string_payload)
        sensor_id = json_payload["sensor_id"]
        data = json_payload["data"]

        if settings.DEBUG:
            logger.debug(f'Topic: {msg.topic} Payload: {json_payload}')

        try:
            sensor = Sensor.objects.select_related('type').get(id=sensor_id)
        except Sensor.DoesNotExist:
            logger.error(f"MQTT: Received data for unknown sensor_id={sensor_id}")
            return

        Data_Received.objects.create(sensor_id=sensor, data=data)

        if sensor.type.type == 'PZEM-004t':
            Data_PZEM004t.objects.create(
                sensor_id=sensor,
                sensor_address=data["address"],
                volts=round(data["voltage"]),
                amps=data["current"],
                frequency=round(data["frequency"]),
                watts=data["power"],
                energy=data["energy"],
                # power factor (0.00 to 1.00) stored as integer 0-100
                power_factor=round(data["pf"] * 100),
            )

    except (KeyError, TypeError, ValueError) as err:
        logger.error(f"MQTT: Invalid payload - {err}. Raw: {msg.payload}")
    except Exception as err:
        logger.error(f"MQTT: Unexpected error processing message - {err}")


client = mqtt.Client(client_id=settings.MQTT_CLIENT_ID)
if settings.MQTT_ACTIVE:
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
    client.connected_flag = False
    client.bad_connection_flag = False
    logger.info(f"MQTT: Connecting to Broker {settings.MQTT_SERVER}, {settings.MQTT_PORT}")
    try:
        client.connect(
            host=settings.MQTT_SERVER,
            port=int(settings.MQTT_PORT),
            keepalive=settings.MQTT_KEEPALIVE,
        )
        client.loop_start()
        logger.debug("MQTT: Loop started")
    except Exception as e:
        logger.error(f"MQTT: Connection failed - {e}")
