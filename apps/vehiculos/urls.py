from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehiculoViewSet

router = DefaultRouter()
router.register(r'vehiculos', VehiculoViewSet, basename='vehiculos')

urlpatterns = [
    path('api/', include(router.urls)),
]
