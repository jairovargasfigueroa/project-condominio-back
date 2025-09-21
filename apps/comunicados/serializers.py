from rest_framework import serializers
from .models import Comunicado


class ComunicadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comunicado
        fields = ['id', 'titulo', 'contenido', 'fecha_publicacion']

    def validate_titulo(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El título no puede estar vacío")
        return value.strip()

    def validate_contenido(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El contenido no puede estar vacío")
        return value.strip()

    def create(self, validated_data):
        raise NotImplementedError("Use ComunicadoService.create_comunicado() instead")

    def update(self, instance, validated_data):
        raise NotImplementedError("Use ComunicadoService.update_comunicado() instead")
