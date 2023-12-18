from django_filters.rest_framework import FilterSet
#from mqttclient.models import *
from sensors.models import *

class SensorDataFilter(FilterSet):
    class Meta:
        model = Data_PZEM004t
        fields = {
            'time': ['gt', 'lt']
        }