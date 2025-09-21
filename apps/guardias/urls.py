# guardias/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GuardiaViewSet

# Crear router automático para generar URLs RESTful
router = DefaultRouter()
router.register(r'guardias', GuardiaViewSet, basename='guardias')

urlpatterns = [
    path('api/', include(router.urls)),
]
