from django.db import models
from django.urls import reverse
from proizvodi.models import Proizvodi
from recepti.models import Recept

# Create your models here.
class DetaljiPretrage(models.Model):
    naziv_detalji    = models.CharField(max_length=120)
    proizvod         = models.ManyToManyField(Proizvodi, blank=True)

    def __str__(self):
        return self.naziv_detalji

    class Meta:
        verbose_name_plural = "Proizvodi Pretraga tags"


class ReceptiPretraga(models.Model):
    trazi             = models.CharField(max_length=120)
    recept            = models.ManyToManyField(Recept, blank=True)

    def __str__(self):
        return self.trazi

    class Meta:
        verbose_name_plural = "Recepti Pretraga tags"


