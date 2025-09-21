from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Count
from apps.accounts.services import UserService
from apps.copropietarios.models import Copropietario


class CopropietarioService:

  @staticmethod
  @transaction.atomic
  def create_copropietario(validated_data):
    """
        Crear copropietario con datos anidados
        validated_data viene con estructura:
        {
            'usuario': { datos del usuario }
        }
    """
    # 1. EXTRAER objeto usuario anidado
    usuario_data = validated_data.pop('usuario')
    usuario_data['rol'] = 'copropietario'

    # 2. Validaciones de negocio específicas de copropietario
    # Aquí puedes agregar validaciones específicas

    usuario = UserService.create_user(usuario_data)

    copropietario = Copropietario.objects.create(
        usuario=usuario
    )

    return copropietario

  @staticmethod
  def get_active_copropietarios():
    """Obtener todos los copropietarios activos con sus usuarios"""
    return Copropietario.objects.select_related('usuario').filter(
        usuario__is_active=True
    ).order_by('id')

  @staticmethod
  def get_copropietario_by_id(copropietario_id):
    """Obtener copropietario por ID"""
    try:
        return Copropietario.objects.select_related('usuario').get(id=copropietario_id)
    except Copropietario.DoesNotExist:
        return None

  @staticmethod
  @transaction.atomic
  def update_copropietario(copropietario, validated_data):
    """
    Actualizar copropietario con validaciones de NEGOCIO
    """
    # Si vienen datos del usuario, actualizarlos
    if 'usuario' in validated_data:
        usuario_data = validated_data.pop('usuario')
        UserService.update_user(copropietario.usuario, usuario_data)

    # Actualizar campos del copropietario
    for field, value in validated_data.items():
        setattr(copropietario, field, value)

    copropietario.save()
    return copropietario

  @staticmethod
  @transaction.atomic
  def delete_copropietario(copropietario):
    """
    Eliminar copropietario (soft delete del usuario)
    """
    # Soft delete del usuario asociado
    copropietario.usuario.is_active = False
    copropietario.usuario.save()

    # También podrías eliminar físicamente el registro del copropietario
    # copropietario.delete()
