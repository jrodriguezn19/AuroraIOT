from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Sensor)
class SensorsAdmin(admin.ModelAdmin):
    fields = ["id", "name"]
    ordering = ["id"]

@admin.register(Sensor_Type)
class SensorType(admin.ModelAdmin):
    ordering = ["type"]


@admin.register(Sensor_Configuration)
class SensorConfiguration(admin.ModelAdmin):
    ordering = ["id"]




