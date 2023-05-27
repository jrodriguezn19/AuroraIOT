from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from sensors.models import Sensor, Data
from .serializers import SensorSerializer, DataSerializer

@api_view()
def sensors_list(request):
    queryset = Sensor.objects.all()
    serializer = SensorSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view()
def sensor_info(request, sensor_id):
    sensor = get_object_or_404(Sensor, pk=sensor_id)
    serializer = SensorSerializer(sensor)
    return Response(serializer.data)


@api_view()
def sensor_data(request, sensor_id):
    queryset = Data.objects.filter(sensor_id=sensor_id)
    serializer = DataSerializer(queryset, many=True)
    return Response(serializer.data)
