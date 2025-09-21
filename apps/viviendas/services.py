from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Vivienda
from apps.categorias.services import CategoriaService


class ViviendaService:

    @staticmethod
    @transaction.atomic
    def create_vivienda(validated_data):
        categoria_id = validated_data.pop('categoria_id')

        categoria = CategoriaService.get_categoria_by_id(categoria_id)
        if not categoria:
            raise ValidationError("La categoría especificada no existe")

        vivienda = Vivienda.objects.create(
            categoria=categoria,
            **validated_data
        )
        return vivienda

    @staticmethod
    def get_active_viviendas():
        return Vivienda.objects.select_related('categoria').all().order_by('numero')

    @staticmethod
    def get_vivienda_by_id(vivienda_id):
        try:
            return Vivienda.objects.select_related('categoria').get(id=vivienda_id)
        except Vivienda.DoesNotExist:
            return None

    @staticmethod
    def get_viviendas_by_categoria(categoria_id):
        return Vivienda.objects.filter(
            categoria_id=categoria_id
        ).select_related('categoria').order_by('numero')

    @staticmethod
    def get_viviendas_by_numero(numero):
        return Vivienda.objects.filter(
            numero__icontains=numero
        ).select_related('categoria').order_by('numero')

    @staticmethod
    @transaction.atomic
    def update_vivienda(vivienda, validated_data):
        categoria_id = validated_data.pop('categoria_id', None)

        if categoria_id:
            categoria = CategoriaService.get_categoria_by_id(categoria_id)
            if not categoria:
                raise ValidationError("La categoría especificada no existe")
            vivienda.categoria = categoria

        for field, value in validated_data.items():
            setattr(vivienda, field, value)
        vivienda.save()
        return vivienda

    @staticmethod
    @transaction.atomic
    def delete_vivienda(vivienda):
        vivienda.delete()

    @staticmethod
    def get_estadisticas():
        total_viviendas = Vivienda.objects.count()
        viviendas_por_categoria = {}

        categorias = CategoriaService.get_active_categorias()
        for categoria in categorias:
            count = Vivienda.objects.filter(categoria=categoria).count()
            viviendas_por_categoria[categoria.nombre] = count

        return {
            'total_viviendas': total_viviendas,
            'viviendas_por_categoria': viviendas_por_categoria,
        }
