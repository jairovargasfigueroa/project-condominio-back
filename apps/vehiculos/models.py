from django.conf import settings
from django.db import models

# Create your models here.

class Vehiculo(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vehiculos'
    )
    placa = models.CharField(max_length=10, unique=True)
    modelo = models.CharField(max_length=100)
    color = models.CharField(max_length=50, blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.placa} - {self.modelo}"
