from django_filters.rest_framework import FilterSet
from mqttclient.models import Data


class SensorDataFilter(FilterSet):
    class Meta:
        model = Data
        fields = {
            'time': ['gt', 'lt']
        }