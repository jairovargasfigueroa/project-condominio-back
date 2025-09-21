from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LecturaComunicadoViewSet

router = DefaultRouter()
router.register(r'lectura-comunicados', LecturaComunicadoViewSet, basename='lectura-comunicados')

urlpatterns = [
    path('api/', include(router.urls)),
]
