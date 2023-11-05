from django.db import models
from sensors.models import Sensor
#Required imports to create generic relations and make this app reusable
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Data(models.Model):
    time = models.DateTimeField(auto_now_add=True, null=False)
    data = models.JSONField(null=True)
    #sensor_id = models.ForeignKey(Sensor, on_delete=models.PROTECT)

    #The required fields to enable a generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) #Sensor class/model #would it better on_delete=models.PROTECT ???
    object_id = models.PositiveIntegerField() #Sensor_id
    content_object = GenericForeignKey("content_type", "object_id") #To read the actual object (Sensor), it could be a Sensor, Actuator, or any device that produce data
    #device = GenericForeignKey("content_type", "object_id") #To read the actual object (Sensor)

