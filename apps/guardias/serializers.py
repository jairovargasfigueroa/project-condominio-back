from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from apps.guardias.models import Guardia


class GuardiaSerializer(serializers.ModelSerializer):
    # Campo anidado para los datos del usuario
    usuario = UserSerializer()

    class Meta:
        model = Guardia
        fields = ['id', 'usuario']

    def validate(self, attrs):
        """Validación a nivel de objeto"""
        # Validaciones cruzadas entre campos si es necesario
        return attrs
