from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from mqttclient.models import Data
# Create your views here.
@api_view()
def sensors_list(request):
    return Response('OK!!!')

def homepage(request):
    # sensors = Sensor.objects.values("name", "brand", "location", "type__type")
    # context = {"sensors": sensors}
    # print(sensors)
    # print(sensors.query)
    # print("\n")

    data = Data.objects.values("sensor_id",
                               "sensor_id__name",
                               "sensor_id__brand", 
                               "sensor_id__type__type", 
                               "sensor_id__location", 
                               "data")
    print(data)
    print(data.query)
    context = {"data":list(data)}
    return render(request, 'index.html', context)