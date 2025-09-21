from django.db import models
from apps.residentes.models import Residente
from apps.comunicados.models import Comunicado


class LecturaComunicado(models.Model):
    residente = models.ForeignKey(
        Residente,
        on_delete=models.CASCADE,
        related_name='lecturas_comunicados',
    )
    comunicado = models.ForeignKey(
        Comunicado,
        on_delete=models.CASCADE,
        related_name='lecturas',
    )
    fecha_lectura = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ('residente', 'comunicado')
        ordering = ['-fecha_lectura']

    def __str__(self):
        return f"{self.residente} leyó '{self.comunicado.titulo}' el {self.fecha_lectura.strftime('%d/%m/%Y')}"
