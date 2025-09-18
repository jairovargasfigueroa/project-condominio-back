from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from apps.residentes.models import Residente


class ResidenteSerializer(serializers.ModelSerializer):
    # Campo anidado para los datos del usuario
    usuario = UserSerializer()

    class Meta:
        model = Residente
        fields = ['id', 'usuario', 'zona']

    def validate_zona(self, value):
        """Validar zona"""
        if not value or not value.strip():
            raise serializers.ValidationError("La zona no puede estar vacía")

        # Aquí puedes agregar más validaciones específicas de zona
        # Por ejemplo: verificar formato, longitud, etc.
        if len(value.strip()) < 1:
            raise serializers.ValidationError("La zona debe tener al menos 1 carácter")

        return value.strip()

    def validate(self, attrs):
        """Validación a nivel de objeto"""
        # Validaciones cruzadas entre campos si es necesario
        return attrs

    def create(self, validated_data):
        """No implementamos create aquí, se maneja en el Service"""
        raise NotImplementedError("Use ResidenteService.create_residente() instead")

    def update(self, instance, validated_data):
        """No implementamos update aquí, se maneja en el Service"""
        raise NotImplementedError("Use ResidenteService.update_residente() instead")


class ResidenteCreateSerializer(serializers.Serializer):
    """Serializer específico para creación de residentes"""
    usuario = UserSerializer()
    zona = serializers.CharField(max_length=100)

    def validate_zona(self, value):
        """Validar zona para creación"""
        if not value or not value.strip():
            raise serializers.ValidationError("La zona no puede estar vacía")
        return value.strip()


class ResidenteUpdateSerializer(serializers.Serializer):
    """Serializer específico para actualización de residentes"""
    usuario = UserSerializer(partial=True, required=False)
    zona = serializers.CharField(max_length=100, required=False)

    def validate_zona(self, value):
        """Validar zona para actualización"""
        if value is not None and (not value or not value.strip()):
            raise serializers.ValidationError("La zona no puede estar vacía")
        return value.strip() if value else value
