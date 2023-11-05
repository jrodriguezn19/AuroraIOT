from django.db import models


class Sensor_Type(models.Model):
    """Type of sensing variable (Temperature, Humidity, etc)"""
    type = models.CharField(max_length=255, unique=True)


class Sensor_Configuration(models.Model):
    description = models.CharField(max_length=255, null=True, default=None)
    update_ms = models.IntegerField(null=False)
    params = models.JSONField(null=True, default=None)


class Sensor(models.Model):
    name = models.CharField(max_length=255, blank=False)
    brand = models.CharField(max_length=255)
    type = models.ForeignKey(Sensor_Type, on_delete=models.PROTECT)
    location = models.CharField(max_length=255)
    sensor_configuration = models.ForeignKey(Sensor_Configuration, null=True, on_delete=models.SET_NULL)




