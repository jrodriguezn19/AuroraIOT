from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('sensors/', views.sensors_list),
    path('sensors/<int:sensor_id>/', views.sensor_info),
    path('sensors/<int:sensor_id>/data', views.sensor_data),

]
