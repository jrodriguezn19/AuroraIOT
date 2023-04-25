from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('sensor', views.sensors_list)
]
