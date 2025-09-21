from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ViviendaViewSet

router = DefaultRouter()
router.register(r'viviendas', ViviendaViewSet, basename='viviendas')

urlpatterns = [
    path('api/', include(router.urls)),
]
