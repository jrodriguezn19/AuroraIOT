#just for testing purposes so I do not create a model in this test app
from sensors.models import Sensor
from sensors.serializers import SensorSerializer

from django.shortcuts import HttpResponse
from django.views.generic import TemplateView

from rest_framework import viewsets
from rest_framework.views import APIView

#Function Based View
def testView(request):
    return HttpResponse("<h1>TEST VIEW</h1>")

#Templateview
#Defined directly in the urls.py

#Class based TemplateView
class ClassTemplateView(TemplateView):
    template_name = "classTemplateView.html"

#Model Viewset
class TestModelViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


