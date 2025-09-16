# residentes/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResidenteViewSet

# Crear router automático para generar URLs RESTful
router = DefaultRouter()
router.register(r'residentes', ResidenteViewSet, basename='residentes')

urlpatterns = [
    path('api/', include(router.urls)),
]
