
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Count
from apps.accounts.services import UserService
from apps.residentes.models import Residente


class ResidenteService:

  @staticmethod
  @transaction.atomic
  def create_residente(validated_data):
    """
        Crear residente con datos anidados
        validated_data viene con estructura:
        {
            'usuario': { datos del usuario },
            'zona': 'A'
        }
    """
    # 1. EXTRAER objeto usuario anidado
    usuario_data = validated_data.pop('usuario')
    usuario_data['rol'] = 'residente'

    # 2. Validaciones de negocio específicas de residente
    zona = validated_data.get('zona')
    if not zona:
        raise ValidationError("La zona es requerida")

    usuario = UserService.create_user(usuario_data)

    residente = Residente.objects.create(
        usuario=usuario,
        zona=zona
    )

    return residente

  @staticmethod
  def get_active_residentes():
    """Obtener todos los residentes activos con sus usuarios"""
    return Residente.objects.select_related('usuario').filter(
        usuario__is_active=True
    ).order_by('id')

  @staticmethod
  def get_residente_by_id(residente_id):
    """Obtener residente por ID"""
    try:
        return Residente.objects.select_related('usuario').get(id=residente_id)
    except Residente.DoesNotExist:
        return None

  @staticmethod
  @transaction.atomic
  def update_residente(residente, validated_data):
    """
    Actualizar residente con validaciones de NEGOCIO
    """
    # Si vienen datos del usuario, actualizarlos
    if 'usuario' in validated_data:
        usuario_data = validated_data.pop('usuario')
        UserService.update_user(residente.usuario, usuario_data)

    # Validación de negocio para zona
    nueva_zona = validated_data.get('zona')
    if nueva_zona and nueva_zona != residente.zona:
        # Aquí puedes agregar validaciones específicas de zona
        pass

    # Actualizar campos del residente
    for field, value in validated_data.items():
        setattr(residente, field, value)

    residente.save()
    return residente

  @staticmethod
  @transaction.atomic
  def delete_residente(residente):
    """
    Eliminar residente (soft delete del usuario)
    """
    # Soft delete del usuario asociado
    residente.usuario.is_active = False
    residente.usuario.save()

    # También podrías eliminar físicamente el registro del residente
    # residente.delete()

  @staticmethod
  def cambiar_zona(residente, nueva_zona):
    """
    Cambiar zona del residente con validaciones
    """
    if not nueva_zona:
        raise ValidationError("La nueva zona es requerida")

    if nueva_zona == residente.zona:
        raise ValidationError("La nueva zona debe ser diferente a la actual")

    # Validaciones adicionales de negocio
    # Por ejemplo: verificar disponibilidad de la zona

    residente.zona = nueva_zona
    residente.save()

    return residente

  @staticmethod
  def get_estadisticas():
    """
    Obtener estadísticas de residentes
    """
    total_residentes = Residente.objects.filter(usuario__is_active=True).count()

    # Estadísticas por zona
    residentes_por_zona = Residente.objects.filter(
        usuario__is_active=True
    ).values('zona').annotate(
        total=Count('id')
    ).order_by('zona')

    return {
        'total_residentes': total_residentes,
        'residentes_por_zona': list(residentes_por_zona),
        'zonas_disponibles': [item['zona'] for item in residentes_por_zona]
    }

  @staticmethod
  def buscar_residentes(query):
    """
    Buscar residentes por nombre, email o zona
    """
    from django.db.models import Q

    return Residente.objects.select_related('usuario').filter(
        usuario__is_active=True
    ).filter(
        Q(usuario__username__icontains=query) |
        Q(usuario__email__icontains=query) |
        Q(usuario__first_name__icontains=query) |
        Q(usuario__last_name__icontains=query) |
        Q(zona__icontains=query)
    ).distinct().order_by('usuario__username')
