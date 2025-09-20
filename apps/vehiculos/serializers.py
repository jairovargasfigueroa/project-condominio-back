from rest_framework import serializers
from django.conf import settings
from .models import Vehiculo


class VehiculoSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)
    usuario_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Vehiculo
        fields = ['id', 'usuario', 'usuario_id', 'placa', 'modelo', 'color', 'marca']

    def validate_placa(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("La placa no puede estar vacía")
        return value.strip().upper()

    def validate_modelo(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El modelo no puede estar vacío")
        return value.strip()

    def create(self, validated_data):
        raise NotImplementedError("Use VehiculoService.create_vehiculo() instead")

    def update(self, instance, validated_data):
        raise NotImplementedError("Use VehiculoService.update_vehiculo() instead")
