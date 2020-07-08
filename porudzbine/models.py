from django.db import models
import uuid
from placanja.models import Placanje
from django.db.models.signals import pre_save, post_save
import math
# Create your models here.

"""
Racunanje jedinstvenog ID za svaku porudzbinu, tako da svaka porudzbina ima jedinstven broj. Za to sam koristio uuid paket. 
Stavio sam da broj porudzbine ima 6 cifara. Na liniji 26 ovo radin gde kazem da je instance.id_porudzbine = str(uuid.uuid4().fields[-1])[:6]
tu zapravo dodeljujem ID od 6 cifara (random ID) novoj narudzbini
"""
STATUSI_NARUCIVANJA_CHOICES = (
    ('created', "Kreirana"),
    ('paid', 'Placena'),
    ('shipped', 'Poslata'),
    )

class Porudzbina(models.Model):
    id_porudzbine    = models.CharField(max_length=240, blank=True)
    status           = models.CharField(max_length=120, default='created', choices=STATUSI_NARUCIVANJA_CHOICES)
    placanje_narudzbina         = models.ForeignKey(Placanje, on_delete=models.CASCADE) #foreign key kako bi stvorili konekciju izmedju Placanja i porudzbina tako da
                                            #jedna porudzbina odgovara jednoj kartici
    postarina_ukupno = models.DecimalField(default=250.00, max_digits=6, decimal_places=2)
    ukupno           = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)

    def __str__(self):
        return self.id_porudzbine

    def dodaj_ukupno(self):
        placanje_ukupno = self.placanje_narudzbina.ukupno
        postarina_ukupno = self.postarina_ukupno
        ukupno_novo = math.fsum([placanje_ukupno, postarina_ukupno]) #ukoliko je jedna cifra decimal a druga float onda izbacuje gresku da ne moze da se sabira sa decimal i float. 
        #Zbog toga se importuje math paket i uz pomoc njega se sabiraju float i decimal i tu cifru posle cuvamo u bazi kao ukupno
        formatirano = format(ukupno_novo, '.2f') #koliko hocemo decimala da ima cifra
        self.ukupno = formatirano
        self.save()
        return ukupno_novo 
         

    class Meta:
        verbose_name_plural = "Porudzbina"

def pre_save_narudzbina_id(sender, instance, *args, **kwarrgs):
    if not instance.id_porudzbine: #proveravamo da vec nemamo id narudzbine za tu narudzbinu i ako nemamo kreiramo noviu
        instance.id_porudzbine = str(uuid.uuid4().fields[-1])[:6]

pre_save.connect(pre_save_narudzbina_id, sender=Porudzbina)

#Racunanje ukupne cifre (svi proizvodi koji su dodati na karticu). Ako neko doda proizvode na karticu pa ode na checkout, pa se vrati nazad
# da doda jos proizvoda ili da izbaci neke, ovaj ispod post save ce apdejtovati total ponovo, tj svaki put kada s epromeni kartica
def post_save_placanje_ukupno(sender, instance, created, *args, **kwargs):
    if not created:
        placanje_object = instance
        plcanje_ukupno  = placanje_object.ukupno
        placanje_id     = placanje_object.id
        qs              = Placanje.objects.filter(proizvodi__id=placanje_id)
        if qs.count() == 1:
            narucivanje_object = qs.first()
            narucivanje_object.dodaj_ukupno()

post_save.connect(post_save_placanje_ukupno, sender=Placanje)

#Ukoliko je narudzbina tek kreirana, tj ako user prvi put kreira narudzbinu:
def post_save_porudzbina(sender, instance, created, *args, **kwargs):
    if created:
        instance.dodaj_ukupno()

post_save.connect(post_save_porudzbina, sender=Porudzbina)