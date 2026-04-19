from django.db import models
from sensors.models import Sensor


class Data_Received(models.Model):
    time = models.DateTimeField(auto_now_add=True, null=False)
    sensor_id = models.ForeignKey(Sensor, on_delete=models.PROTECT)
    data = models.JSONField(null=True)

    def __str__(self) -> str:
        return f"{self.time}"

    class Meta:
        indexes = [
            models.Index(fields=['sensor_id', '-time'], name='data_received_sensor_time_idx'),
        ]
