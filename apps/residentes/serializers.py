from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from apps.residentes.models import Residente


class ResidenteSerializer(serializers.Serializer):
  usuario = UserSerializer();

  class Meta:
    model = Residente
    fields = '__all__'
