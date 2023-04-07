from django.db import models


# Create your models here.
class Sensor_Type(models.Model):
    sensor_type = models.CharField(max_length=255)


class Sensor(models.Model):
    sensor_reference = models.CharField(max_length=255)
    sensor_type = models.ForeignKey(Sensor_Type, on_delete=models.PROTECT)
    sensor_brand = models.CharField(max_length=255)
