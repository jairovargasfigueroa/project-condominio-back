from django.conf import settings
from django.db import models

# Create your models here.
class Guardia(models.Model):
  usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='guardia_profile'
    )

  def __str__(self):
    return f"Guardia: {self.usuario.get_full_name()}"
