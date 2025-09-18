# mascotas/services.py
from django.db import transaction
from django.core.exceptions import ValidationError
from apps.residentes.models import Residente
from .models import Mascota


class MascotaService:
    """Service para lógica de negocio de mascotas"""

    @staticmethod
    @transaction.atomic
    def create_mascota(validated_data):
        """Crear mascota con validaciones de NEGOCIO"""
        # Manejar residente_data (crear residente anidado) o residente_id
        residente_data = validated_data.pop('residente_data', None)
        residente_id = validated_data.pop('residente_id', None)

        if residente_data:
            # Crear residente anidado usando ResidenteService
            from apps.residentes.services import ResidenteService
            residente = ResidenteService.create_residente(residente_data)
        elif residente_id:
            # Usar residente existente
            try:
                residente = Residente.objects.get(id=residente_id, usuario__is_active=True)
            except Residente.DoesNotExist:
                raise ValidationError("El residente especificado no existe o no está activo")
        else:
            raise ValidationError("Debe proporcionar residente_id o residente_data")

        # Crear mascota
        mascota = Mascota.objects.create(
            residente=residente,
            **validated_data
        )
        return mascota

    @staticmethod
    def get_active_mascotas():
        """Obtener todas las mascotas"""
        return Mascota.objects.select_related(
            'residente__usuario'
        ).all().order_by('nombre')

    @staticmethod
    def get_mascota_by_id(mascota_id):
        """Obtener mascota por ID"""
        try:
            return Mascota.objects.select_related(
                'residente__usuario'
            ).get(id=mascota_id)
        except Mascota.DoesNotExist:
            return None

    @staticmethod
    def get_mascotas_by_residente(residente_id):
        """Obtener mascotas de un residente específico"""
        return Mascota.objects.filter(
            residente_id=residente_id
        ).order_by('nombre')

    @staticmethod
    @transaction.atomic
    def update_mascota(mascota, validated_data):
        """Actualizar mascota"""
        for field, value in validated_data.items():
            setattr(mascota, field, value)
        mascota.save()
        return mascota

    @staticmethod
    @transaction.atomic
    def delete_mascota(mascota):
        """Eliminar mascota"""
        mascota.delete()

    @staticmethod
    def get_estadisticas():
        """Obtener estadísticas básicas de mascotas"""
        total_mascotas = Mascota.objects.count()
        return {
            'total_mascotas': total_mascotas,
        }
