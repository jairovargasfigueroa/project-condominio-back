from rest_framework import serializers
from .models import Vivienda
from apps.categorias.serializers import CategoriaSerializer
from apps.categorias.models import Categoria
from apps.copropietarios.models import Copropietario
from apps.copropietarios.serializers import CopropietarioSerializer


class ViviendaSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.IntegerField(write_only=True, required=True)

    copropietario = CopropietarioSerializer(read_only=True)
    copropietario_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Vivienda
        fields = ['id', 'categoria', 'categoria_id', 'copropietario', 'copropietario_id', 'numero', 'direccion']

    def validate_numero(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El número no puede estar vacío")
        return value.strip()

    def validate_direccion(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("La dirección no puede estar vacía")
        return value.strip()

    def validate_categoria_id(self, value):
        if value:
            try:
                categoria = Categoria.objects.get(id=value)
                return value
            except Categoria.DoesNotExist:
                raise serializers.ValidationError("La categoría especificada no existe")
        return value

    def validate_copropietario_id(self, value):
        if value:
            try:
                copropietario = Copropietario.objects.get(id=value)
                return value
            except Copropietario.DoesNotExist:
                raise serializers.ValidationError("El copropietario especificado no existe")
        return value

    def create(self, validated_data):
        raise NotImplementedError("Use ViviendaService.create_vivienda() instead")

    def update(self, instance, validated_data):
        raise NotImplementedError("Use ViviendaService.update_vivienda() instead")
