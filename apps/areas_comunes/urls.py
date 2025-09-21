from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AreaComunViewSet

router = DefaultRouter()
router.register(r'areas-comunes', AreaComunViewSet, basename='areas-comunes')

urlpatterns = [
    path('api/', include(router.urls)),
]
