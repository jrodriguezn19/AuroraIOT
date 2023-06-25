from django.urls import path, include
from . import views
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('sensors', views.SensorViewSet, basename="sensors")

sensors_router = routers.NestedDefaultRouter(router, 'sensors', lookup='sensor_pk')
sensors_router.register('data', views.SensorDataViewset, basename='sensor-data')

# URLConf
#urlpatterns = router.urls + sensors_router.urls
urlpatterns = [
    path('', include(router.urls)),
    path('', include(sensors_router.urls)),
]

# urlpatterns = [
#     path('', include(router.urls)),
#     path('sensors/<int:pk>/data', views.SensorData.as_view()),
#     # path('sensors/', views.SensorList.as_view()),
#     # path('sensors/<int:pk>/', views.SensorInfo.as_view()),
# ]
