from django.db import models


class Vivienda(models.Model):
    categoria = models.ForeignKey('categorias.Categoria', on_delete=models.CASCADE, related_name='viviendas')
    numero = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return f"Vivienda {self.numero} - {self.direccion}"

