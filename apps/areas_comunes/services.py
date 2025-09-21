from django.db import transaction
from django.core.exceptions import ValidationError
from .models import AreaComun


class AreaComunService:

    @staticmethod
    @transaction.atomic
    def create_area_comun(validated_data):
        area_comun = AreaComun.objects.create(**validated_data)
        return area_comun

    @staticmethod
    def get_active_areas_comunes():
        return AreaComun.objects.all().order_by('nombre')

    @staticmethod
    def get_area_comun_by_id(area_id):
        try:
            return AreaComun.objects.get(id=area_id)
        except AreaComun.DoesNotExist:
            return None

    @staticmethod
    def get_areas_by_tipo(tipo):
        return AreaComun.objects.filter(tipo=tipo).order_by('nombre')

    @staticmethod
    @transaction.atomic
    def update_area_comun(area_comun, validated_data):
        for field, value in validated_data.items():
            setattr(area_comun, field, value)
        area_comun.save()
        return area_comun

    @staticmethod
    @transaction.atomic
    def delete_area_comun(area_comun):
        area_comun.delete()

    @staticmethod
    def get_estadisticas():
        total_areas = AreaComun.objects.count()
        areas_gratuitas = AreaComun.objects.filter(tipo='gratuita').count()
        areas_pago = AreaComun.objects.filter(tipo='pago').count()
        return {
            'total_areas': total_areas,
            'areas_gratuitas': areas_gratuitas,
            'areas_pago': areas_pago,
        }
