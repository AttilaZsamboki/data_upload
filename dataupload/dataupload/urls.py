from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register('/uploadmodel', views.UploadmodelViewSet,
                basename="uploadmodel")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('frontend.urls')),
    path(r'api', include(router.urls))
]
