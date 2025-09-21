# copropietarios/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CopropietarioViewSet

# Crear router automático para generar URLs RESTful
router = DefaultRouter()
router.register(r'copropietarios', CopropietarioViewSet, basename='copropietarios')

urlpatterns = [
    path('api/', include(router.urls)),
]
