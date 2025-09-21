# administradores/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdministradorViewSet

# Crear router automático para generar URLs RESTful
router = DefaultRouter()
router.register(r'administradores', AdministradorViewSet, basename='administradores')

urlpatterns = [
    path('api/', include(router.urls)),
]
