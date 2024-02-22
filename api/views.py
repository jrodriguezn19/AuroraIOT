from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from sensors.models import *
from .serializers import SensorSerializer, DataPZEM004tSerializer
from .filters import SensorDataFilter

class SensorViewSet(ModelViewSet):
    queryset = Sensor.objects.all().order_by('id')
    serializer_class = SensorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name', 'brand']

class SensorDataViewSet(ModelViewSet):
    queryset = Data_PZEM004t.objects.all().order_by('id')
    serializer_class = DataPZEM004tSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = SensorDataFilter
    lookup_field = 'id' 

    def get_queryset(self):
        sensor_pk = self.kwargs['sensor_pk']
        return self.queryset.filter(sensor_id=sensor_pk)
