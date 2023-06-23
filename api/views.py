from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from sensors.models import Sensor, Data
from .serializers import SensorSerializer, DataSerializer


class SensorList(ListAPIView):
    queryset= Sensor.objects.all()
    serializer_class = SensorSerializer
    
    # def get(self, request):
    #     queryset = Sensor.objects.all()
    #     serializer = SensorSerializer(queryset, many=True)
    #     return Response(serializer.data)
    
#Function based view
# @api_view(['GET'])
# def sensors_list(request):
#     queryset = Sensor.objects.all()
#     serializer = SensorSerializer(queryset, many=True)
#     return Response(serializer.data)

class SensorInfo(RetrieveAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    # def get(self, request, sensor_id):
    #     sensor = get_object_or_404(Sensor, pk=sensor_id)
    #     serializer = SensorSerializer(sensor)
    #     return Response(serializer.data)

#Function based view    
# @api_view(['GET'])
# def sensor_info(request, sensor_id):
#     sensor = get_object_or_404(Sensor, pk=sensor_id)
#     serializer = SensorSerializer(sensor)
#     return Response(serializer.data)

class SensorData(ListAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

    # def get(self, request, sensor_id):
    #     queryset = Data.objects.filter(sensor_id=sensor_id)
    #     serializer = DataSerializer(queryset, many=True)
    #     return Response(serializer.data)

#Function based view 
# @api_view(['GET'])
# def sensor_data(request, sensor_id):
#     queryset = Data.objects.filter(sensor_id=sensor_id)
#     serializer = DataSerializer(queryset, many=True)
#     return Response(serializer.data)
