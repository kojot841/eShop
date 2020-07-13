from django.conf import settings
from django.db import models
from proizvodi.models import Proizvodi
from django.db.models.signals import pre_save, post_save, m2m_changed

Korisnik = settings.AUTH_USER_MODEL

# Create your models here.

class PlacanjeManager(models.Manager): 

    def id_kreiranje(self, request):
        id_placanja     = request.session.get('placanje_id', None) #Uzimamo id placanja iz sesije, broj koji je povezan sa objektom u bazi (models-id), ako ga nemamo onda uzmi None
        id              = self.get_queryset().filter(id=id_placanja) #ako imamo ID proveri da li postoji u bazi. U model menadzeru mozemo da radmo .get_queryset() a to je isto kao sto smo uradili Placanje.objects.filter
        if id.count()   == 1: # ako postoji id u bazi onda dodeli sesiji taj ID iz baze
            novi_id=False
            placanje_obj = id.first()
            if request.user.is_authenticated and placanje_obj.user is None:
                """ 
                User krene da kupuje kao gost (nije ulogovan) doda proizvode na karticu i nakon toga se uloguje. Svi proizvodi koje je dodao kao
                gost ce biti sacuvani i kada se bude ulogovao. tj. sesija ili id sesije ce biti povezan sa njegovim profilom u bazi 
                to rade ove dve linije ispod
                """
                placanje_obj.user = request.user
                placanje_obj.save()
        else:
            placanje_obj = Placanje.objects.novi_id(user=request.user)#ako ID ne postoji ili nije 1 (ima ih vise za isto placanje) onda kreiraj novi i dodeli sesiji
            novi_id=True
            request.session['placanje_id'] = placanje_obj.id
        return placanje_obj, novi_id

    #ovaj metod kreira novi ID placanja ako user nije authenticated, ako jeste onda ne kreira novi ID. 
    def novi_id(self, user=None):
        user_obj        = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class PlacanjeKolicina(models.Model):
    proizvod = models.ForeignKey(Proizvodi,on_delete=models.CASCADE)
    kolicina_proizvoda = models.IntegerField(default=1)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    def __unicode__(self):
        return self.proizvod.naziv

    def __str__(self):
        return str(self.proizvod.naziv)

    class Meta:
        verbose_name_plural = "PlacanjeKolicina"

class Placanje(models.Model):
    kolicina             = models.ManyToManyField(PlacanjeKolicina, blank=True)
    user                 = models.ForeignKey(Korisnik, null=True, blank=True, on_delete=models.CASCADE) #ovde dodajem null=true i blank=true da bi i 
                                                                    # non authenticated user ili guest user mogao da placa tj dodaje proizvode na karticu ili kreira karticu
    proizvodi            = models.ManyToManyField(Proizvodi, blank=True) #ovde dodajem blank=True kako bi bilo moguce imati praznu karticu
    postarina            = models.IntegerField(default=250)
    ukupno_bez_postarine = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    ukupno_sa_postarinom = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    izmena               = models.DateTimeField(auto_now=True) #da bi znali kada je kartica poslednji put izmenjena
    vreme                = models.DateTimeField(auto_now_add=True) # da bi znali kada je model kreiran
    

    objects = PlacanjeManager()

    def __str__(self):
        return str(self.id) #vracamo iD kartice ili placanja

    class Meta:
        verbose_name_plural = "Placanja"

#Ovo je signal za placanje, tj kada dodamo proizvode za placanje ovaj signal ce da izracuna total nakon sto smo dodali proizvode. 
# Ovo sve isto moze da se uradi i u view.
#Ovaj pre_save receiver se poziva kad se sacuva u bazi, tj kada dodamo proizvode na placanje i kliknemo na save poziva se ovaj
# pre-save receiver koji u mom slucaju racuna sumu dodatih proizvoda i cuva tu sumu kao zbir u bazi
def pre_save_placanje(sender, instance, action, *args, **kwargs):
    if action == 'pre_remove' or action == 'pre_add' or action == 'post_remove' or action == 'post_add': #action je po django dokumentaciji parametar koji uzima m2m signal i samo jedan od metoda je post_save i Post_remove, postoji jos mnogo metoda
                                                        #ja sam samo ta dva ukljucio posto u mom slucaju cu ili ddoavati proizvode ili ih uklanjati
       
        # proizvodi       = instance.proizvodi.all()
        # ukupno          = 0
        # for proizvod in proizvodi:
        #     ukupno += proizvod.cena
        # instance.ukupno = ukupno
        # instance.save()
        pass

m2m_changed.connect(pre_save_placanje, sender=Placanje.proizvodi.through) #ovo je iz django dokumentacije, da kada se koristi m2m signal sender je naziv klase, naziv m2m fields (proizvodi) i na kraju rec through
#posto je model placanje many-to-many field onda moramo koristiti m2m signal umesto pre_save ili post_save

def racunanje_postarine(sender, instance, *args, **kwargs):
    pass
    # if instance.ukupno > 0:
    #     instance.postarina = 250
    #     instance.ukupno_sa_postarinom = instance.ukupno + instance.postarina
    # else:
    #     instance.postarina = 0
    #     instance.ukupno_sa_postarinom = instance.ukupno

pre_save.connect(racunanje_postarine, sender=PlacanjeKolicina)
