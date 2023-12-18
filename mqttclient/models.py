from django.db import models
from sensors.models import Sensor
#Required imports to create generic relations and make this app reusable
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType


class Data_Received(models.Model):
    time = models.DateTimeField(auto_now_add=True, null=False)
    sensor_id = models.ForeignKey(Sensor, on_delete=models.PROTECT)
    data = models.JSONField(null=True)

    # #Required fields to enable a generic relation
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) #Sensor class/model #would it better on_delete=models.PROTECT ???
    # object_id = models.PositiveIntegerField() # equivalent to sensor_id
    # content_object = GenericForeignKey("content_type", "object_id") #This is the actual value in the table (Sensor), it could be a Sensor, Actuator, or any device that produce data
    # #device = GenericForeignKey("content_type", "object_id") #To read the actual object (Sensor)

# class Data_Sent(models.model):
#     time = models.DateTimeField(auto_now_add=True, null=False)
#     data_sent = models.JSONField(null=True)