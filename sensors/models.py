from django.db import models
#Timescale Imports
from timescale.db.models.fields import TimescaleDateTimeField
from timescale.db.models.managers import TimescaleManager
from django.utils.timezone import now

class Sensor_Type(models.Model):
    """Type of sensing variable (Temperature, Humidity, etc)"""
    type = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.type}"
    
    class Meta:
        verbose_name = "Sensor Type"


class Sensor_Configuration(models.Model):
    description = models.CharField(max_length=255, null=True, default=None)
    update_ms = models.IntegerField(null=False)
    params = models.JSONField(null=True, blank=True, default=None)

    def __str__(self) -> str:
        return f"{self.description}"
    
    class Meta:
        verbose_name = "Configuration"


class Sensor(models.Model):
    name = models.CharField(max_length=255, blank=False)
    brand = models.CharField(max_length=255)
    type = models.ForeignKey(Sensor_Type, on_delete=models.PROTECT)
    location = models.CharField(max_length=255)
    sensor_configuration = models.ForeignKey(
        Sensor_Configuration, null=True, on_delete=models.SET_NULL)
    
    def __str__(self) -> str:
        return f"{self.id} - {self.name}"


class TimescaleModel(models.Model):
    """
    A helper class for using Timescale within Django, has the TimescaleManager and
    TimescaleDateTimeField already present. This is an abstract class it should
    be inheritted by another class for use.
    """
    time = TimescaleDateTimeField(interval="1 day", default=now)
    objects = TimescaleManager()

    class Meta:
        abstract = True


class Data_PZEM004t(TimescaleModel):
    """
    Model to store data in a structured way. This option require a 
    a new data table per each sensor due to the difference in data readings structure
    """
    #time field is already created in the abstract base class for Timescale
    #time = models.DateTimeField(auto_now_add=True, null=False)
    sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    sensor_address = models.PositiveSmallIntegerField()
    # V
    volts = models.PositiveSmallIntegerField()
    # A
    amps = models.DecimalField(max_digits=5, decimal_places=2)
    # Hz
    frequency = models.PositiveSmallIntegerField()
    # W
    watts = models.DecimalField(max_digits=6, decimal_places=2)
    # kWh
    energy = models.DecimalField(max_digits=6, decimal_places=2)
    # power factor (0.00 to 1.00) is multiplied by 100 to store integer values (0 to 100).
    power_factor = models.PositiveSmallIntegerField()
