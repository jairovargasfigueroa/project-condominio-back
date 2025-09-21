from django.db import models
from django.core.validators import MinValueValidator


class AreaComun(models.Model):
    TIPO_CHOICES = [
        ('gratuita', 'Gratuita'),
        ('pago', 'De Pago'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='gratuita')
    costo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)]
    )


    def __str__(self):
        if self.tipo == 'pago':
            return f"{self.nombre} - ${self.costo}"
        return f"{self.nombre} - Gratuita"
