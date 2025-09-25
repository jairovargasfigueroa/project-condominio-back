from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Count
from apps.accounts.services import UserService
from apps.guardias.models import Guardia


class GuardiaService:

    @staticmethod
    @transaction.atomic
    def create_guardia(validated_data):
        """
        Crear guardia con datos anidados
        validated_data viene con estructura:
        {
            'usuario': { datos del usuario }
        }
        """
        # 1. EXTRAER objeto usuario anidado
        usuario_data = validated_data.pop('usuario')
        usuario_data['rol'] = 'guardia'

        # 2. Validaciones de negocio específicas de guardia
        # Aquí puedes agregar validaciones específicas

        usuario = UserService.create_user(usuario_data)

        guardia = Guardia.objects.create(
            usuario=usuario
        )

        return guardia

    @staticmethod
    def get_active_guardias():
        """Obtener todos los guardias activos con sus usuarios"""
        return Guardia.objects.select_related('usuario').filter(
            usuario__is_active=True
        ).order_by('id')

    @staticmethod
    def get_guardia_by_id(guardia_id):
        """Obtener guardia por ID"""
        try:
            return Guardia.objects.select_related('usuario').get(id=guardia_id)
        except Guardia.DoesNotExist:
            return None

    @staticmethod
    def get_guardia_by_user(user):
        """Obtener guardia por usuario autenticado"""
        try:
            return Guardia.objects.select_related('usuario').get(usuario=user)
        except Guardia.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def update_guardia(guardia, validated_data):
        """
        Actualizar guardia con validaciones de NEGOCIO
        """
        # Si vienen datos del usuario, actualizarlos
        if 'usuario' in validated_data:
            usuario_data = validated_data.pop('usuario')
            UserService.update_user(guardia.usuario, usuario_data)

        # Actualizar campos del guardia
        for field, value in validated_data.items():
            setattr(guardia, field, value)

        guardia.save()
        return guardia

    @staticmethod
    @transaction.atomic
    def delete_guardia(guardia):
        """
        Eliminar guardia (soft delete del usuario)
        """
        # Soft delete del usuario asociado
        guardia.usuario.is_active = False
        guardia.usuario.save()

        return True

    @staticmethod
    def count_guardias():
        """Contar guardias activos"""
        return Guardia.objects.filter(usuario__is_active=True).count()

    @staticmethod
    def search_guardias(query):
        """Buscar guardias por nombre o email"""
        return Guardia.objects.select_related('usuario').filter(
            usuario__is_active=True
        ).filter(
            usuario__first_name__icontains=query
        ) | Guardia.objects.select_related('usuario').filter(
            usuario__is_active=True
        ).filter(
            usuario__last_name__icontains=query
        ) | Guardia.objects.select_related('usuario').filter(
            usuario__is_active=True
        ).filter(
            usuario__email__icontains=query
        ).order_by('id')
