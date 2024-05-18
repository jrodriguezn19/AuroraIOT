# from django.urls import path
# from . import views

# # URLConf
# urlpatterns = [
#     path('', views.sensors_homepage),
# ]

from django.urls import path, include
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('sensors', views.SensorViewSet, basename="sensors")

sensors_router = routers.NestedDefaultRouter(router, r'sensors', lookup='sensor')
sensors_router.register(r'data', views.SensorDataViewSet, basename='sensor-data')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(sensors_router.urls)),
]


