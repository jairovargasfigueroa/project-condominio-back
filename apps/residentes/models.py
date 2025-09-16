from django.conf import settings
from django.db import models



# Create your models here.
class Residente(models.Model):

  usuario = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='residente_profile')
  zona = models.CharField(max_length=100)



