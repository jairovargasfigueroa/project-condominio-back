from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Vivienda
from apps.categorias.services import CategoriaService
from apps.copropietarios.services import CopropietarioService


class ViviendaService:

    @staticmethod
    @transaction.atomic
    def create_vivienda(validated_data):
        categoria_id = validated_data.pop('categoria_id')
        copropietario_id = validated_data.pop('copropietario_id', None)

        categoria = CategoriaService.get_categoria_by_id(categoria_id)
        if not categoria:
            raise ValidationError("La categoría especificada no existe")

        copropietario = None
        if copropietario_id:
            copropietario = CopropietarioService.get_copropietario_by_id(copropietario_id)
            if not copropietario:
                raise ValidationError("El copropietario especificado no existe")

        vivienda = Vivienda.objects.create(
            categoria=categoria,
            copropietario=copropietario,
            **validated_data
        )
        return vivienda

    @staticmethod
    def get_active_viviendas():
        return Vivienda.objects.select_related('categoria', 'copropietario__usuario').all().order_by('numero')

    @staticmethod
    def get_vivienda_by_id(vivienda_id):
        try:
            return Vivienda.objects.select_related('categoria', 'copropietario__usuario').get(id=vivienda_id)
        except Vivienda.DoesNotExist:
            return None

    @staticmethod
    def get_viviendas_by_categoria(categoria_id):
        return Vivienda.objects.filter(
            categoria_id=categoria_id
        ).select_related('categoria', 'copropietario__usuario').order_by('numero')

    @staticmethod
    def get_viviendas_by_numero(numero):
        return Vivienda.objects.filter(
            numero__icontains=numero
        ).select_related('categoria', 'copropietario__usuario').order_by('numero')

    @staticmethod
    def get_viviendas_sin_propietario():
        """Obtener viviendas que no tienen copropietario asignado"""
        return Vivienda.objects.filter(
            copropietario__isnull=True
        ).select_related('categoria').order_by('numero')

    @staticmethod
    def get_viviendas_by_copropietario(copropietario_id):
        """Obtener todas las viviendas de un copropietario específico"""
        return Vivienda.objects.filter(
            copropietario_id=copropietario_id
        ).select_related('categoria', 'copropietario__usuario').order_by('numero')

    @staticmethod
    @transaction.atomic
    def update_vivienda(vivienda, validated_data):
        categoria_id = validated_data.pop('categoria_id', None)
        copropietario_id = validated_data.pop('copropietario_id', None)

        if categoria_id:
            categoria = CategoriaService.get_categoria_by_id(categoria_id)
            if not categoria:
                raise ValidationError("La categoría especificada no existe")
            vivienda.categoria = categoria

        # Manejar copropietario (puede ser None para quitar propietario)
        if 'copropietario_id' in validated_data or copropietario_id is not None:
            if copropietario_id:
                copropietario = CopropietarioService.get_copropietario_by_id(copropietario_id)
                if not copropietario:
                    raise ValidationError("El copropietario especificado no existe")
                vivienda.copropietario = copropietario
            else:
                # Si copropietario_id es None, quitar el propietario
                vivienda.copropietario = None

        for field, value in validated_data.items():
            setattr(vivienda, field, value)
        vivienda.save()
        return vivienda

    @staticmethod
    @transaction.atomic
    def asignar_copropietario(vivienda_id, copropietario_id):
        """Asignar un copropietario a una vivienda específica"""
        vivienda = ViviendaService.get_vivienda_by_id(vivienda_id)
        if not vivienda:
            raise ValidationError("La vivienda especificada no existe")

        if copropietario_id:
            copropietario = CopropietarioService.get_copropietario_by_id(copropietario_id)
            if not copropietario:
                raise ValidationError("El copropietario especificado no existe")
            vivienda.copropietario = copropietario
        else:
            vivienda.copropietario = None

        vivienda.save()
        return vivienda

    @staticmethod
    @transaction.atomic
    def delete_vivienda(vivienda):
        vivienda.delete()

    @staticmethod
    def get_estadisticas():
        total_viviendas = Vivienda.objects.count()
        viviendas_con_propietario = Vivienda.objects.filter(copropietario__isnull=False).count()
        viviendas_sin_propietario = Vivienda.objects.filter(copropietario__isnull=True).count()

        viviendas_por_categoria = {}

        categorias = CategoriaService.get_active_categorias()
        for categoria in categorias:
            count = Vivienda.objects.filter(categoria=categoria).count()
            viviendas_por_categoria[categoria.nombre] = count

        return {
            'total_viviendas': total_viviendas,
            'viviendas_con_propietario': viviendas_con_propietario,
            'viviendas_sin_propietario': viviendas_sin_propietario,
            'viviendas_por_categoria': viviendas_por_categoria,
        }
