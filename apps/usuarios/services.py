# usuarios/services.py
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import CustomUser

class UserService:
    """Service para lógica de negocio de usuarios"""
    
    @staticmethod
    def create_user(validated_data):
        """
        Crear usuario con validaciones de NEGOCIO
        (El serializer ya validó el FORMATO)
        """
        # Validación de NEGOCIO: email único en BD
        email = validated_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Este email ya está registrado")
        
        # Validación de NEGOCIO: username único en BD
        username = validated_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Este username ya está en uso")
        
        # Extraer password (lógica de negocio)
        password = validated_data.pop('password')
        
        # Crear usuario usando el manager de Django
        user = CustomUser.objects.create_user(password=password, **validated_data)
        
        # Lógica de negocio adicional futura:
        # - Enviar email de bienvenida
        # - Crear configuraciones por defecto
        # - Log de auditoría
        
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        """Obtener usuario por ID"""
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None
    
    @staticmethod
    def update_user(user, validated_data):
        """
        Actualizar usuario con validaciones de NEGOCIO
        """
        # Validación de NEGOCIO: email único (excluyendo usuario actual)
        new_email = validated_data.get('email')
        if new_email and new_email != user.email:
            if CustomUser.objects.filter(email=new_email).exists():
                raise ValidationError("Este email ya está en uso")
        
        # Validación de NEGOCIO: username único (excluyendo usuario actual)
        new_username = validated_data.get('username')
        if new_username and new_username != user.username:
            if CustomUser.objects.filter(username=new_username).exists():
                raise ValidationError("Este username ya está en uso")
        
        # Actualizar campos
        password = validated_data.pop('password', None)
        for field, value in validated_data.items():
            setattr(user, field, value)
        
        # Lógica especial para password
        if password:
            user.set_password(password)  # Hash automático
        
        user.save()
        return user
    
    @staticmethod
    def authenticate_user(username, password):
        """
        Autenticar usuario con lógica de negocio adicional
        """
        # Intentar autenticación por username
        user = authenticate(username=username, password=password)
        
        # Lógica de negocio: también permitir login por email
        if not user:
            try:
                user_obj = CustomUser.objects.get(email=username)
                user = authenticate(username=user_obj.username, password=password)
            except CustomUser.DoesNotExist:
                pass
        
        # Validación de negocio: usuario debe estar activo
        if user and not user.is_active:
            return None
        
        return user
    
    @staticmethod
    def get_active_users():
        """Obtener usuarios activos - lógica de negocio"""
        return CustomUser.objects.filter(is_active=True).order_by('-date_joined')
    
    @staticmethod
    def delete_user(user_id):
        """
        Eliminar usuario con lógica de negocio
        """
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise ValidationError("Usuario no encontrado")
        # Lógica de negocio: soft delete en lugar de hard delete
        user.is_active = False
        user.save()
        # Futuro: limpiar datos relacionados, notificar sistemas externos, etc.
        return True