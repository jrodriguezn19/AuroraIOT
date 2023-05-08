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



# '''
# Model idea to store data in a structured way. This would require a 
# a new data table per each sensor due to the difference in data readings structure
# class Energy_Data(models.Model):
#     time = models.DateTimeField(auto_now_add=True, null=False)
#     sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE)
#     # V
#     volts = models.PositiveSmallIntegerField()
#     # A
#     amps = models.PositiveSmallIntegerField()
#     # Hz
#     frequency = models.PositiveSmallIntegerField()
#     # W
#     watts = models.PositiveSmallIntegerField()
#     # kWh
#     energy = models.PositiveIntegerField
#     # power factor (0.00 to 1.00) is multiplied by 100 to store integer values (0 to 100).
#     power_factor = models.PositiveSmallIntegerField()
# '''