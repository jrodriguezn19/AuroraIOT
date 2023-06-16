from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('sensors/', views.SensorList.as_view()),
    path('sensors/<int:sensor_id>/', views.SensorInfo.as_view()),
    path('sensors/<int:sensor_id>/data', views.SensorData.as_view()),

]
