from django.shortcuts import render
from .models import *
from sensors.models import Data


def sensors_homepage(request):
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
    return render(request, 'sensors.html', context)