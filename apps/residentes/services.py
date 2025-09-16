


from django.db import transaction
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
            'numero_apartamento': '501',
            'torre': 'A',
            'fecha_ingreso': '2025-01-01'
        }
    """

    # 1. EXTRAER objeto usuario anidado
    usuario_data = validated_data.pop('usuario')
    usuario_data['rol'] = 'residente'

    usuario = UserService.create_user(usuario_data)

    zona = validated_data.pop('zona')

    residente = Residente.objects.create(
      usuario = usuario,
      zona = zona
      )

    return residente

  @staticmethod
  def get_active_residentes():
    """Obtener todos los residentes activos con sus usuarios"""
    return Residente.objects.select_related('usuario').all().order_by('id')

  @staticmethod
  def get_residente_by_usuario(residente_id):
    try:
      return Residente.objects.select_related('usuario').get(id = residente_id)
    except Residente.DoesNotExist:
      return None
