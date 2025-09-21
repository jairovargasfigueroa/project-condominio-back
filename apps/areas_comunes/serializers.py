from rest_framework import serializers
from .models import AreaComun


class AreaComunSerializer(serializers.ModelSerializer):

    class Meta:
        model = AreaComun
        fields = ['id', 'nombre', 'tipo', 'costo']

    def validate_nombre(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío")
        return value.strip()

    def validate_costo(self, value):
        if value < 0:
            raise serializers.ValidationError("El costo no puede ser negativo")
        return value

    def validate(self, attrs):
        tipo = attrs.get('tipo')
        costo = attrs.get('costo', 0)

        if tipo == 'gratuita' and costo > 0:
            attrs['costo'] = 0.00
        elif tipo == 'pago' and costo == 0:
            raise serializers.ValidationError("Las áreas de pago deben tener un costo mayor a 0")

        return attrs

    def create(self, validated_data):
        raise NotImplementedError("Use AreaComunService.create_area_comun() instead")

    def update(self, instance, validated_data):
        raise NotImplementedError("Use AreaComunService.update_area_comun() instead")
