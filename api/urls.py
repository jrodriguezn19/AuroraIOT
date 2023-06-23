from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('sensors/', views.SensorList.as_view()),
    path('sensors/<int:pk>/', views.SensorInfo.as_view()),
    path('sensors/<int:pk>/data', views.SensorData.as_view()),

]
