from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('administrador', 'Administrador'),
        ('residente', 'Residente'),
        ('copropietario', 'Copropietario'),
        ('guardia', 'Guardia'),
        ('visitante', 'Visitante'),
    ]

    telefono = models.CharField(max_length=20, blank=True, null=True)  # campo adicional opcional
    fecha_nacimiento = models.DateField(blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROLE_CHOICES, default='residente')


# # Configurar para login con email
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []  # Campos requeridos además del USERNAME_FIELD
    def __str__(self):
        return self.username
