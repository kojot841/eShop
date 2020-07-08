from django.views.generic import ListView, DetailView
from django.shortcuts import render, Http404
from .models import Proizvodi, ProizvodiMenadzer
from django.db.models import Q
from detalji_za_pretragu.models import DetaljiPretrage

from placanja.models import Placanje


class ProizvodiPregled(ListView):
    queryset      = Proizvodi.objects.all()
    template_name = 'proizvodi/proizvodi.html'


class ProizvodiDetaljanPregled(DetailView):
    queryset        = Proizvodi.objects.all()
    template_name   = 'proizvodi/proizvodi_detaljno.html'

    def get_context_data(self, *args, **kwargs):  #Metod mora da se zove get_context_data, ako se drugacije zove ne radi nista!!
        #Klasa DetailView vec ima ugradjen metod get_context_data i zato mora tako da se zove ako njega pozivamo.
        context                 = super(ProizvodiDetaljanPregled, self).get_context_data(*args, **kwargs)
        placanje_obj, novi_obj  = Placanje.objects.id_kreiranje(self.request)
        context['placanja']     = placanje_obj
        return context
    

class Pretraga(ListView):
    template_name = 'proizvodi/pretraga.html'

    def get_queryset(self, *args, **kwargs):
        request     = self.request
        query       = request.GET.get('q')
        if query is not None:
            lookups = (Q(naziv__icontains=query) | 
                      Q(opis__icontains=query) | 
                      Q(cena__icontains=query) | 
                      Q(detaljipretrage__naziv_detalji__icontains=query))
            return Proizvodi.objects.filter(lookups).distinct()
        return Proizvodi.objects.none()