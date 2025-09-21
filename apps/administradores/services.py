from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Count
from apps.accounts.services import UserService
from apps.administradores.models import Administrador


class AdministradorService:

    @staticmethod
    @transaction.atomic
    def create_administrador(validated_data):
        """
        Crear administrador con datos anidados
        validated_data viene con estructura:
        {
            'usuario': { datos del usuario }
        }
        """
        # 1. EXTRAER objeto usuario anidado
        usuario_data = validated_data.pop('usuario')
        usuario_data['rol'] = 'administrador'

        # 2. Validaciones de negocio específicas de administrador
        # Aquí puedes agregar validaciones específicas

        usuario = UserService.create_user(usuario_data)

        administrador = Administrador.objects.create(
            usuario=usuario
        )

        return administrador

    @staticmethod
    def get_active_administradores():
        """Obtener todos los administradores activos con sus usuarios"""
        return Administrador.objects.select_related('usuario').filter(
            usuario__is_active=True
        ).order_by('id')

    @staticmethod
    def get_administrador_by_id(administrador_id):
        """Obtener administrador por ID"""
        try:
            return Administrador.objects.select_related('usuario').get(id=administrador_id)
        except Administrador.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def update_administrador(administrador, validated_data):
        """
        Actualizar administrador con validaciones de NEGOCIO
        """
        # Si vienen datos del usuario, actualizarlos
        if 'usuario' in validated_data:
            usuario_data = validated_data.pop('usuario')
            UserService.update_user(administrador.usuario, usuario_data)

        # Actualizar campos del administrador
        for field, value in validated_data.items():
            setattr(administrador, field, value)

        administrador.save()
        return administrador

    @staticmethod
    @transaction.atomic
    def delete_administrador(administrador):
        """
        Eliminar administrador (soft delete del usuario)
        """
        # Soft delete del usuario asociado
        administrador.usuario.is_active = False
        administrador.usuario.save()

        return True

    @staticmethod
    def count_administradores():
        """Contar administradores activos"""
        return Administrador.objects.filter(usuario__is_active=True).count()

    @staticmethod
    def search_administradores(query):
        """Buscar administradores por nombre o email"""
        return Administrador.objects.select_related('usuario').filter(
            usuario__is_active=True
        ).filter(
            usuario__first_name__icontains=query
        ) | Administrador.objects.select_related('usuario').filter(
            usuario__is_active=True
        ).filter(
            usuario__last_name__icontains=query
        ) | Administrador.objects.select_related('usuario').filter(
            usuario__is_active=True
        ).filter(
            usuario__email__icontains=query
        ).order_by('id')
