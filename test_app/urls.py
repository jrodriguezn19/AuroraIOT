from django.urls import path
from django.views.generic import TemplateView
from .views import *
#router import
from rest_framework.routers import DefaultRouter

# URLConf
urlpatterns = [
    path('testview/', testView),
    #The view TemplateView is defined here
    path('templateview/', TemplateView.as_view(template_name="templateViewPage.html")),
    path('classtemplateview/', ClassTemplateView.as_view()),
]

router = DefaultRouter()
#Model Viewset
router.register(r'testmodelviewset', TestModelViewSet)


#This is how I include routers and the normal way of defining the url paths
urlpatterns += router.urls

#If ony have routers I can do this
#urlpatterns = router.urls




