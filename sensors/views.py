from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
from sensors.models import *
from .serializers import SensorSerializer, DataPZEM004tSerializer
from .filters import SensorDataFilter

class SensorViewSet(ReadOnlyModelViewSet):
    queryset = Sensor.objects.all().order_by('id')
    serializer_class = SensorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name', 'brand']

class SensorDataViewSet(ReadOnlyModelViewSet):
    #.order_by('time') is required to avoid pagination inconsistencies.
    # A warning raised if not present
    queryset = Data_PZEM004t.objects.all()#.order_by('id')
    serializer_class = DataPZEM004tSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = SensorDataFilter
    #field to find individual instances of the model, aka: data in an specific time
    lookup_field = 'id' 
    # available fields to order
    ordering_fields = ["time"]
    # default ordering
    #ordering = ["id"]

    def get_queryset(self):
        sensor_pk = self.kwargs['sensor_pk']
        return self.queryset.filter(sensor_id=sensor_pk)


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