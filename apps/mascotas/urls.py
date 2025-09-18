# mascotas/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MascotaViewSet

# Crear router automático para generar URLs RESTful
router = DefaultRouter()
router.register(r'mascotas', MascotaViewSet, basename='mascotas')

urlpatterns = [
    path('api/', include(router.urls)),
]
