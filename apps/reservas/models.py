from django.db import models

# Create your models here.
class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    ]

    METODO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('qr', 'QR'),
    ]

    residente = models.ForeignKey('residentes.Residente', on_delete=models.CASCADE)
    area_comun = models.ForeignKey('areas_comunes.AreaComun', on_delete=models.CASCADE)
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='pendiente')
    metodo_pago = models.CharField(max_length=10, choices=METODO_PAGO_CHOICES, null=True, blank=True)
