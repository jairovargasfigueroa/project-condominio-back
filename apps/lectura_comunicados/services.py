from django.db import transaction, models
from django.core.exceptions import ValidationError
from .models import LecturaComunicado
from apps.residentes.models import Residente
from apps.comunicados.models import Comunicado


class LecturaComunicadoService:

    @staticmethod
    @transaction.atomic
    def marcar_como_leido(residente_id, comunicado_id):
        """Marca un comunicado como leído por un residente"""
        try:
            residente = Residente.objects.get(id=residente_id)
            comunicado = Comunicado.objects.get(id=comunicado_id)
        except (Residente.DoesNotExist, Comunicado.DoesNotExist):
            raise ValidationError("Residente o comunicado no encontrado")

        # Verificar si ya fue marcado como leído
        if LecturaComunicado.objects.filter(residente=residente, comunicado=comunicado).exists():
            raise ValidationError("Este comunicado ya fue marcado como leído por el residente")

        lectura = LecturaComunicado.objects.create(
            residente=residente,
            comunicado=comunicado
        )
        return lectura

    @staticmethod
    def verificar_lectura(residente_id, comunicado_id):
        """Verifica si un residente leyó un comunicado específico"""
        return LecturaComunicado.objects.filter(
            residente_id=residente_id,
            comunicado_id=comunicado_id
        ).exists()

    @staticmethod
    def get_lecturas_por_comunicado(comunicado_id):
        """Obtiene todas las lecturas de un comunicado específico"""
        return LecturaComunicado.objects.filter(
            comunicado_id=comunicado_id
        ).select_related('residente').order_by('-fecha_lectura')

    @staticmethod
    def get_lecturas_por_residente(residente_id):
        """Obtiene todas las lecturas de un residente específico"""
        return LecturaComunicado.objects.filter(
            residente_id=residente_id
        ).select_related('comunicado').order_by('-fecha_lectura')

    @staticmethod
    def get_estadisticas_comunicado(comunicado_id):
        """Obtiene estadísticas de lectura de un comunicado"""
        total_residentes = Residente.objects.count()
        lecturas = LecturaComunicado.objects.filter(comunicado_id=comunicado_id).count()

        porcentaje_lectura = (lecturas / total_residentes * 100) if total_residentes > 0 else 0

        return {
            'total_residentes': total_residentes,
            'residentes_que_leyeron': lecturas,
            'residentes_sin_leer': total_residentes - lecturas,
            'porcentaje_lectura': round(porcentaje_lectura, 2)
        }

    @staticmethod
    def get_comunicados_no_leidos_por_residente(residente_id):
        """Obtiene comunicados que un residente no ha leído"""
        comunicados_leidos = LecturaComunicado.objects.filter(
            residente_id=residente_id
        ).values_list('comunicado_id', flat=True)

        return Comunicado.objects.exclude(
            id__in=comunicados_leidos
        ).order_by('-fecha_publicacion')

    @staticmethod
    def get_residentes_sin_leer_comunicado(comunicado_id):
        """Obtiene residentes que no han leído un comunicado específico"""
        residentes_que_leyeron = LecturaComunicado.objects.filter(
            comunicado_id=comunicado_id
        ).values_list('residente_id', flat=True)

        return Residente.objects.exclude(
            id__in=residentes_que_leyeron
        )

    @staticmethod
    def get_estadisticas_generales():
        """Obtiene estadísticas generales del sistema"""
        total_comunicados = Comunicado.objects.count()
        total_residentes = Residente.objects.count()
        total_lecturas = LecturaComunicado.objects.count()

        promedio_lecturas_por_comunicado = (
            total_lecturas / total_comunicados
        ) if total_comunicados > 0 else 0

        return {
            'total_comunicados': total_comunicados,
            'total_residentes': total_residentes,
            'total_lecturas': total_lecturas,
            'promedio_lecturas_por_comunicado': round(promedio_lecturas_por_comunicado, 2)
        }
