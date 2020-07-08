from django.db import models
from django.urls import reverse


class ProizvodiMenadzer(models.Model):
    def get_by_id(self,id):
        queryset = self.get_queryset().filter(id=id)
        if queryset.count()==1:
            return queryset.first()
        return None

class Proizvodi(models.Model):
    naziv       = models.CharField(max_length=120)
    opis        = models.TextField()
    cena        = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    slika       = models.ImageField(null=True, blank=True)


    objects = ProizvodiMenadzer()

    def url(self):
        # return '{pk}/'.format(pk=self.pk)
        return reverse('proizvodi_detalji', kwargs={'pk':self.pk})

    def __str__(self):
        return self.naziv

    def __unicode__(self):
        return self.naziv

    class Meta:
        verbose_name_plural = "Proizvodi"