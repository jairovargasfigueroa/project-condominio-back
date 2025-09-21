from rest_framework import serializers
from datetime import date, time
from .models import Reserva
from apps.residentes.models import Residente
from apps.areas_comunes.models import AreaComun
from apps.residentes.serializers import ResidenteSerializer
from apps.areas_comunes.serializers import AreaComunSerializer


class ReservaSerializer(serializers.ModelSerializer):
    residente = ResidenteSerializer(read_only=True)
    area_comun = AreaComunSerializer(read_only=True)
    residente_id = serializers.IntegerField(write_only=True, required=False)
    area_comun_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Reserva
        fields = ['id', 'residente', 'area_comun', 'residente_id', 'area_comun_id',
                 'fecha_reserva', 'hora_inicio', 'hora_fin', 'monto_pagado', 'estado', 'metodo_pago']

    def validate_fecha_reserva(self, value):
        if value < date.today():
            raise serializers.ValidationError("No se pueden hacer reservas en fechas pasadas")
        return value

    def validate_hora_fin(self, value):
        hora_inicio = self.initial_data.get('hora_inicio')
        if hora_inicio and value <= time.fromisoformat(hora_inicio):
            raise serializers.ValidationError("La hora de fin debe ser posterior a la hora de inicio")
        return value

    def validate_residente_id(self, value):
        if value:
            try:
                residente = Residente.objects.get(id=value)
                if not residente.usuario.is_active:
                    raise serializers.ValidationError("El residente no está activo")
                return value
            except Residente.DoesNotExist:
                raise serializers.ValidationError("El residente especificado no existe")
        return value

    def validate_area_comun_id(self, value):
        if value:
            try:
                area = AreaComun.objects.get(id=value)
                return value
            except AreaComun.DoesNotExist:
                raise serializers.ValidationError("El área común especificada no existe")
        return value

    def validate(self, attrs):
        residente_id = attrs.get('residente_id')
        area_comun_id = attrs.get('area_comun_id')
        estado = attrs.get('estado')
        metodo_pago = attrs.get('metodo_pago')

        if not self.instance:
            if not residente_id:
                raise serializers.ValidationError("Debe proporcionar residente_id")
            if not area_comun_id:
                raise serializers.ValidationError("Debe proporcionar area_comun_id")

        if estado == 'confirmada' and not metodo_pago:
            raise serializers.ValidationError("Las reservas confirmadas deben tener un método de pago")

        return attrs

    def create(self, validated_data):
        raise NotImplementedError("Use ReservaService.create_reserva() instead")

    def update(self, instance, validated_data):
        raise NotImplementedError("Use ReservaService.update_reserva() instead")
