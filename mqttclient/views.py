import json
from django.http import JsonResponse
from mqttclient.mqtt import client as mqtt_client

#To publish (send) messages to the MQTT Broker
# def publish_message(request):
#     '''Send data via MQTT to the broker'''
#     request_data = json.loads(request.body)
#     rc, mid = mqtt_client.publish(request_data['topic'], request_data['msg'])
#     return JsonResponse({'code': rc})
