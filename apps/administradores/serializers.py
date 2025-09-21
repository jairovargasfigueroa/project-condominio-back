from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from apps.administradores.models import Administrador


class AdministradorSerializer(serializers.ModelSerializer):
    # Campo anidado para los datos del usuario
    usuario = UserSerializer()

    class Meta:
        model = Administrador
        fields = ['id', 'usuario']

    def validate(self, attrs):
        """Validación a nivel de objeto"""
        # Validaciones cruzadas entre campos si es necesario
        return attrs
