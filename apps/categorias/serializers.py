from rest_framework import serializers
from .models import Categoria


class CategoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'tarifa_mensual']

    def validate_nombre(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío")
        return value.strip()

    def validate_tarifa_mensual(self, value):
        if value < 0:
            raise serializers.ValidationError("La tarifa mensual no puede ser negativa")
        return value

    def create(self, validated_data):
        raise NotImplementedError("Use CategoriaService.create_categoria() instead")

    def update(self, instance, validated_data):
        raise NotImplementedError("Use CategoriaService.update_categoria() instead")
