from rest_framework import serializers

from apps.residentes.serializers import ResidenteSerializer

from .models import Mascota


class MascotaSerializer(serializers.Serializer):
  residente = ResidenteSerializer()

  class Meta:
    model = Mascota
    fields = '__all__'
