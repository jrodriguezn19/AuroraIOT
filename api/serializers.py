from rest_framework import serializers
from sensors.models import Sensor, Data

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        #fields = '__all__' #All fields shouldn't be exposed by default, just what is needed
        fields = ['id','name', 'brand', 'location', 'type', 'sensor_configuration']

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        # fields = '__all__'
        fields = ['id', 'sensor_id', 'time', 'data']

    
    


