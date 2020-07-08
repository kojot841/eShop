from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL

class Recept(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    post     = models.TextField(max_length=600)
    kreirano = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Recepti"
