# accounts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

# Crear router automático
router = DefaultRouter()
router.register(r'usuarios', UserViewSet, basename='users')

urlpatterns = [
    path('api/', include(router.urls)),
]
