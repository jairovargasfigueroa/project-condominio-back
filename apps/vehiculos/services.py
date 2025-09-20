from django.db import transaction
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import Vehiculo


class VehiculoService:

    @staticmethod
    @transaction.atomic
    def create_vehiculo(validated_data):
        usuario_id = validated_data.pop('usuario_id', None)

        if usuario_id:
            try:
                User = settings.AUTH_USER_MODEL
                from django.contrib.auth import get_user_model
                user = get_user_model().objects.get(id=usuario_id, is_active=True)
            except get_user_model().DoesNotExist:
                raise ValidationError("El usuario especificado no existe o no está activo")
        else:
            raise ValidationError("Debe proporcionar usuario_id")

        vehiculo = Vehiculo.objects.create(
            usuario=user,
            **validated_data
        )
        return vehiculo

    @staticmethod
    def get_active_vehiculos():
        return Vehiculo.objects.select_related('usuario').all().order_by('placa')

    @staticmethod
    def get_vehiculo_by_id(vehiculo_id):
        try:
            return Vehiculo.objects.select_related('usuario').get(id=vehiculo_id)
        except Vehiculo.DoesNotExist:
            return None

    @staticmethod
    def get_vehiculos_by_usuario(usuario_id):
        return Vehiculo.objects.filter(usuario_id=usuario_id).order_by('placa')

    @staticmethod
    @transaction.atomic
    def update_vehiculo(vehiculo, validated_data):
        for field, value in validated_data.items():
            setattr(vehiculo, field, value)
        vehiculo.save()
        return vehiculo

    @staticmethod
    @transaction.atomic
    def delete_vehiculo(vehiculo):
        vehiculo.delete()

    @staticmethod
    def get_estadisticas():
        total_vehiculos = Vehiculo.objects.count()
        return {
            'total_vehiculos': total_vehiculos,
        }
