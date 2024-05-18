from rest_framework import serializers
from sensors.models import *
from mqttclient.models import *

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        #fields = '__all__' #All fields shouldn't be exposed by default, expose just what is needed
        fields = ['id','name', 'brand', 'location', 'type', 'sensor_configuration']

class DataPZEM004tSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data_PZEM004t
        #fields = '__all__' #All fields shouldn't be exposed by default, expose just what is needed
        fields = ['id', 'sensor_id', 'time', 'volts', 'amps', 'frequency', 'watts', 'energy', 'power_factor', ]
