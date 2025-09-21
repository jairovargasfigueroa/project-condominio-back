from django.db import transaction, models
from django.core.exceptions import ValidationError
from .models import Categoria


class CategoriaService:

    @staticmethod
    @transaction.atomic
    def create_categoria(validated_data):
        categoria = Categoria.objects.create(**validated_data)
        return categoria

    @staticmethod
    def get_active_categorias():
        return Categoria.objects.all().order_by('nombre')

    @staticmethod
    def get_categoria_by_id(categoria_id):
        try:
            return Categoria.objects.get(id=categoria_id)
        except Categoria.DoesNotExist:
            return None

    @staticmethod
    def get_categoria_by_nombre(nombre):
        try:
            return Categoria.objects.get(nombre__iexact=nombre)
        except Categoria.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def update_categoria(categoria, validated_data):
        for field, value in validated_data.items():
            setattr(categoria, field, value)
        categoria.save()
        return categoria

    @staticmethod
    @transaction.atomic
    def delete_categoria(categoria):
        categoria.delete()

    @staticmethod
    def get_estadisticas():
        total_categorias = Categoria.objects.count()
        tarifa_promedio = Categoria.objects.aggregate(
            promedio=models.Avg('tarifa_mensual')
        )['promedio'] or 0
        tarifa_maxima = Categoria.objects.aggregate(
            maxima=models.Max('tarifa_mensual')
        )['maxima'] or 0
        tarifa_minima = Categoria.objects.aggregate(
            minima=models.Min('tarifa_mensual')
        )['minima'] or 0

        return {
            'total_categorias': total_categorias,
            'tarifa_promedio': round(float(tarifa_promedio), 2),
            'tarifa_maxima': float(tarifa_maxima),
            'tarifa_minima': float(tarifa_minima),
        }
