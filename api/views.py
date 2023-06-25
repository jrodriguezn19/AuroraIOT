from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from sensors.models import Sensor, Data
from .serializers import SensorSerializer, DataSerializer

class SensorViewSet(ModelViewSet):
    queryset = Sensor.objects.all().order_by('id')
    serializer_class = SensorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name', 'brand']
    
class SensorDataViewset(ModelViewSet):
    queryset = Data.objects.all().order_by('id')
    serializer_class = DataSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['sensor_id']
