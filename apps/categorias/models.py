from django.db import models
from django.core.validators import MinValueValidator


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    tarifa_mensual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )


    def __str__(self):
        return f"{self.nombre} - ${self.tarifa_mensual}"

