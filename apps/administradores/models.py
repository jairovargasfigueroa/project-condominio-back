from django.db import models
from django.conf import settings



# Create your models here.

class Administrador(models.Model):

  usuario = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='administrador_profile')
  