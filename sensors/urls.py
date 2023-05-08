from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('', views.homepage),
    path('sensors_list/', views.sensors_list)
]
