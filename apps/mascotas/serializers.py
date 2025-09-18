from rest_framework import serializers
from apps.residentes.serializers import ResidenteSerializer
from apps.residentes.models import Residente
from .models import Mascota


class MascotaSerializer(serializers.ModelSerializer):
    # Campo anidado para mostrar información del residente (solo lectura)
    residente = ResidenteSerializer(read_only=True)

    # Campo para recibir datos del residente en creación (solo escritura)
    residente_data = serializers.DictField(write_only=True, required=False)

    # Campo para recibir el ID del residente en creación/actualización
    residente_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Mascota
        fields = ['id', 'residente', 'residente_data', 'residente_id', 'nombre', 'raza', 'color']

    def validate(self, attrs):
        """Validar que se proporcione residente_id o residente_data"""
        residente_data = attrs.get('residente_data')
        residente_id = attrs.get('residente_id')

        # Solo validar en creación
        if not self.instance:
            if not residente_data and not residente_id:
                raise serializers.ValidationError(
                    "Debe proporcionar 'residente_id' o 'residente_data'"
                )

        return attrs

    def validate_residente_id(self, value):
        """Validar que el residente existe y está activo"""
        if value:
            try:
                residente = Residente.objects.get(id=value)
                if not residente.usuario.is_active:
                    raise serializers.ValidationError("El residente no está activo")
                return value
            except Residente.DoesNotExist:
                raise serializers.ValidationError("El residente especificado no existe")
        return value

    def validate_nombre(self, value):
        """Validar nombre de la mascota"""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío")
        return value.strip()

    def create(self, validated_data):
        """No implementamos create aquí, se maneja en el Service"""
        raise NotImplementedError("Use MascotaService.create_mascota() instead")

    def update(self, instance, validated_data):
        """No implementamos update aquí, se maneja en el Service"""
        raise NotImplementedError("Use MascotaService.update_mascota() instead")
