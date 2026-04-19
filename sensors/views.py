from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
from sensors.models import Sensor, Data_PZEM004t
from .serializers import SensorSerializer, DataPZEM004tSerializer
from .filters import SensorDataFilter
from .pagination import SensorDataCursorPagination

class SensorViewSet(ReadOnlyModelViewSet):
    queryset = Sensor.objects.all().order_by('id')
    serializer_class = SensorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name', 'brand']

class SensorDataViewSet(ReadOnlyModelViewSet):
    serializer_class = DataPZEM004tSerializer
    pagination_class = SensorDataCursorPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = SensorDataFilter

    def get_queryset(self):
        return (
            Data_PZEM004t.objects
            .filter(sensor_id=self.kwargs['sensor_pk'])
            .order_by('-time')
        )
