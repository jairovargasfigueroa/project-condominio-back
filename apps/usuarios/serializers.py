# usuarios/serializers.py
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'telefono', 'fecha_nacimiento', 'password', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'date_joined': {'read_only': True},
        }

    def validate_telefono(self, value):
        """Validar formato de teléfono"""
        if value and not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("Formato de teléfono inválido")
        return value

    def validate_email(self, value):
        """Validar formato básico de email"""
        if '@' not in value or '.' not in value:
            raise serializers.ValidationError("Formato de email inválido")
        return value