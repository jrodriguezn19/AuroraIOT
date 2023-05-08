from django.db import models
from sensors.models import Sensor

class Data(models.Model):
    time = models.DateTimeField(auto_now_add=True, null=False)
    sensor_id = models.ForeignKey(Sensor, on_delete=models.PROTECT)
    data = models.JSONField(null=True)

