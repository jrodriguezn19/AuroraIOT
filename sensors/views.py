from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
from sensors.models import Sensor, Data_PZEM004t
from .serializers import SensorSerializer, DataPZEM004tSerializer
from .filters import SensorDataFilter

class SensorViewSet(ReadOnlyModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name', 'brand']

class SensorDataViewSet(ReadOnlyModelViewSet):
    """
    Read sensor data for a specific sensor. Ordered by timestamp.
    """
    serializer_class = DataPZEM004tSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = SensorDataFilter

    # Use natural key if you want URLs like `/sensors/<pk>/data/2023-07-01T12:00:00Z/`
    lookup_field = 'time'            # or keep default PK
    ordering_fields = ['time']
    ordering = ['-time']             # newest first by default
        
    def get_queryset(self):
        return (
            Data_PZEM004t.objects
            .filter(sensor_id=self.kwargs['sensor_pk'])
            .select_related('sensor_id')
            .order_by('-time')
        )




# from django.shortcuts import render
# from .models import *
# from mqttclient.models import *


# def sensors_homepage(request):
#     # sensors = Sensor.objects.values("name", "brand", "location", "type__type")
#     # context = {"sensors": sensors}
#     # print(sensors)
#     # print(sensors.query)
#     # print("\n")

#     data = Data_Received.objects.values(
#         "time",
#         "sensor_id",
#         "sensor_id__name",
#         "sensor_id__brand",
#         "sensor_id__type__type",
#         "sensor_id__location",
#         "data",
#     ).order_by("-id")[:20]
#     # print(data.query)
#     context = {"data": list(data)}
#     return render(request, "sensors.html", context)