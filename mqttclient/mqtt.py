import json
import logging

import paho.mqtt.client as mqtt
from django.conf import settings

from sensors.models import Sensor, Data_PZEM004t
from mqttclient.models import Data_Received

logger = logging.getLogger(__name__)

_client = None  # module-level reference prevents GC after start() returns


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        logger.info(f'MQTT: Connected successfully, returned code = {rc}')
        client.subscribe('auroraiot/#', qos=1)
    else:
        logger.error(f'MQTT: Bad connection, returned code = {rc}')
        client.bad_connection_flag = True


def on_disconnect(client, userdata, rc):
    logger.warning(f"MQTT: Disconnected with result code {rc}")
    client.connected_flag = False
    # Reconnection is handled automatically by loop_start() via
    # reconnect_delay_set(). Do not call reconnect() here — doing so
    # from the callback thread causes competing reconnect storms when
    # multiple workers share the same client_id.


def on_message(mqtt_client, userdata, msg):
    try:
        string_payload = msg.payload.decode('utf8').replace("'", '"')

        if string_payload == "ESP32 Connected to MQTT Broker":
            return

        try:
            json_payload = json.loads(string_payload)
        except ValueError:
            # Non-JSON diagnostic messages (ping, timestamp, etc.) on non-energy topics are expected
            if msg.topic != 'auroraiot/energy':
                return
            raise
        sensor_id = json_payload["sensor_id"]
        data = json_payload["data"]

        logger.info(f'MQTT: Message on topic={msg.topic}')

        try:
            sensor = Sensor.objects.select_related('type').get(id=sensor_id)
        except Sensor.DoesNotExist:
            logger.error(f"MQTT: Received data for unknown sensor_id={sensor_id}")
            return

        Data_Received.objects.create(sensor_id=sensor, data=data)

        if sensor.type.type == 'Energy':
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


def start():
    global _client
    _client = mqtt.Client(client_id=settings.MQTT_CLIENT_ID)
    client = _client
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
    client.connected_flag = False
    client.bad_connection_flag = False
    # Let Paho handle reconnection automatically with exponential backoff
    client.reconnect_delay_set(min_delay=1, max_delay=60)
    logger.info(f"MQTT: Connecting to broker {settings.MQTT_SERVER}:{settings.MQTT_PORT}")
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
