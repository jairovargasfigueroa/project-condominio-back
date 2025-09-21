from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComunicadoViewSet

router = DefaultRouter()
router.register(r'comunicados', ComunicadoViewSet, basename='comunicados')

urlpatterns = [
    path('api/', include(router.urls)),
]
