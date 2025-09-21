from django.db import transaction, models
from django.core.exceptions import ValidationError
from .models import Comunicado


class ComunicadoService:

    @staticmethod
    @transaction.atomic
    def create_comunicado(validated_data):
        comunicado = Comunicado.objects.create(**validated_data)
        return comunicado

    @staticmethod
    def get_all_comunicados():
        return Comunicado.objects.all().order_by('-fecha_publicacion')

    @staticmethod
    def get_comunicado_by_id(comunicado_id):
        try:
            return Comunicado.objects.get(id=comunicado_id)
        except Comunicado.DoesNotExist:
            return None

    @staticmethod
    def get_comunicados_by_titulo(titulo):
        return Comunicado.objects.filter(titulo__icontains=titulo).order_by('-fecha_publicacion')

    @staticmethod
    @transaction.atomic
    def update_comunicado(comunicado, validated_data):
        for field, value in validated_data.items():
            setattr(comunicado, field, value)
        comunicado.save()
        return comunicado

    @staticmethod
    @transaction.atomic
    def delete_comunicado(comunicado):
        comunicado.delete()

    @staticmethod
    def get_comunicados_recientes(limit=10):
        return Comunicado.objects.all().order_by('-fecha_publicacion')[:limit]

    @staticmethod
    def get_estadisticas():
        total_comunicados = Comunicado.objects.count()
        comunicados_este_mes = Comunicado.objects.filter(
            fecha_publicacion__month=models.functions.Extract('now', 'month'),
            fecha_publicacion__year=models.functions.Extract('now', 'year')
        ).count()

        return {
            'total_comunicados': total_comunicados,
            'comunicados_este_mes': comunicados_este_mes
        }
