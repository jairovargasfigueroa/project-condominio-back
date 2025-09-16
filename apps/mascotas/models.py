from django.db import models

# Create your models here.

class Mascota(models.Model):
  residente = models.ForeignKey(
    'residentes.Residente',
    on_delete=models.CASCADE,
    related_name='mascotas'
    )

  nombre = models.CharField(max_length=100)
  raza = models.CharField(max_length=100, blank=True, null=True)
  color = models.CharField(max_length=100, blank=True, null=True)

