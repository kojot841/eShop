from django.shortcuts import render, redirect
from .models import Placanje, PlacanjeKolicina
from proizvodi.models import Proizvodi
from porudzbine.models import Porudzbina
from django.conf import settings
from django.core.mail import send_mail
from .forms import Checkout_Pouzece
from django.contrib import messages
import math
 

# Create your views here.
    
def placanje(request):
    placanje_obj, novi_id = Placanje.objects.id_kreiranje(request) #posto model vraca nazad placanje_obj i novi_id, onda oba moram staviti u ovoj liniji
    return render(request, 'placanja/placanja_pocetna.html', {'placanja':placanje_obj})  

def azuriranje_proizvoda(request):
    id_proizvoda = request.POST.get('id_proizvoda') #Sakriveni deo html forme nam vraca id_proizvoda svaki put kada kliknemo da dodamo na karticu proizvod i onda taj ID proizvoda mozemo uzeti
    try:
        the_id = request.session['placanje_id']
    except:
       nova_kartica = Placanje()
       nova_kartica.save()
       request.session['placanje_id'] = nova_kartica.id
       the_id = nova_kartica.id


    try:
        qty = request.POST.get('qty')
        update_qty = True
    except:
        qty = None
        update_qty = False

    kartica = Placanje.objects.get(id=the_id)

    if id_proizvoda is not None:
        try:
            proizvod = Proizvodi.objects.get(id=id_proizvoda) #uzmi proizvod, tj probaj da ga uzmes ako ga ima tj ako nije None
        except Proizvodi.DoesNotExist:
            #print('Proizvod ne postoji')
            return redirect("placanje:pocetna") #vracamo ih na pocetnu stranicu placanja
        placanje_obj, novi_id = Placanje.objects.id_kreiranje(request) #uzmi instance sa kojom trenutno radimo ili kreiraj novu 
        kartica_kolicina, kreirano_kolicina = PlacanjeKolicina.objects.get_or_create(proizvod=proizvod)
        if kartica_kolicina in kartica.kolicina.all():
            pass
            # kartica.kolicina.remove(kartica_kolicina)
        else:    
            kartica.kolicina.add(kartica_kolicina) #dodaj proizvod u many2many field tj dodaj relaciju u many2many field izmedju instance i proizvoda
            #ne mora da se stavi save jer imamo signal u modelu za many2many change koji automatski sejvuje
        #request.session['broj_proizvoda'] = placanje_obj.proizvodi.count() #pokazuje broj proizvoda na kartici, tj racina broj u modelu
    
        if update_qty and qty:
            if int(qty) == 0:
                kartica_kolicina.delete()
            else:
                kartica_kolicina.kolicina_proizvoda = qty
                kartica_kolicina.save()
    
    new_total = 0
    suma = 0
    for item in kartica.kolicina.all():
        line_total = float(item.proizvod.cena) * item.kolicina_proizvoda
        new_total += line_total
        item.total = line_total
        suma       += item.total
        item.save()
    # item.save()

    # print("Suma je", suma)
    # item.totalukupno = suma
    # formatirano = round(suma)
    # item.totalukupno = formatirano
    # item.save()
    # print("Suma je", formatirano)
    # print("Item total ukupno je", item.totalukupno)
    postarina = 250
    for item in Placanje.objects.all():
        item.ukupno_bez_postarine = suma
        sa_postarinom = suma + postarina
        item.ukupno_sa_postarinom = sa_postarinom
        item.save()
       
    


    #ukupno_novo = math.fsum([item.totalukupno, suma]) #ukoliko je jedna cifra decimal a druga float onda izbacuje gresku da ne moze da se sabira sa decimal i float. 
        #Zbog toga se importuje math paket i uz pomoc njega se sabiraju float i decimal i tu cifru posle cuvamo u bazi kao ukupno
    #    formatirano = format(ukupno_novo, '.2f')
    # suma = 0
    # for total in kartica.kolicina.all():
    #     suma += total.total
    # print('suma je', suma)


    return redirect("placanje:pocetna")


# def brisanje(request):
#     id_proizvoda = request.POST.get('id_proizvoda') #Sakriveni deo html forme nam vraca id_proizvoda svaki put kada kliknemo da dodamo na karticu proizvod i onda taj ID proizvoda mozemo uzeti
#     try:
#         the_id = request.session['placanje_id']
#     except:
#        nova_kartica = Placanje()
#        nova_kartica.save()
#        request.session['placanje_id'] = nova_kartica.id
#        the_id = nova_kartica.id


#     try:
#         qty = request.POST.get('qty')
#         update_qty = True
#     except:
#         qty = None
#         update_qty = False

#     kartica = Placanje.objects.get(id=the_id)
#     print("Id priizvoda je,", id_proizvoda)

#     if id_proizvoda is not None:
#         try:
#             proizvod = Proizvodi.objects.get(id=id_proizvoda) #uzmi proizvod, tj probaj da ga uzmes ako ga ima tj ako nije None
#         except Proizvodi.DoesNotExist:
#             #print('Proizvod ne postoji')
#             return redirect("placanje:pocetna") #vracamo ih na pocetnu stranicu placanja
#         placanje_obj, novi_id = Placanje.objects.id_kreiranje(request) #uzmi instance sa kojom trenutno radimo ili kreiraj novu 
#         kartica_kolicina, kreirano_kolicina = PlacanjeKolicina.objects.get_or_create(proizvod=proizvod)
#         if kartica_kolicina in kartica.kolicina.all():
           
#             kartica.kolicina.remove(kartica_kolicina)
#         else:    
#             pass
#             #kartica.kolicina.add(kartica_kolicina) #dodaj proizvod u many2many field tj dodaj relaciju u many2many field izmedju instance i proizvoda
#             #ne mora da se stavi save jer imamo signal u modelu za many2many change koji automatski sejvuje
#         #request.session['broj_proizvoda'] = placanje_obj.proizvodi.count() #pokazuje broj proizvoda na kartici, tj racina broj u modelu
    
#         if update_qty and qty:
#             if int(qty) == 0:
#                 kartica_kolicina.delete()
#             else:
#                 kartica_kolicina.kolicina_proizvoda = qty
#                 kartica_kolicina.save()
    
#     new_total = 0
#     suma = 0
#     for item in kartica.kolicina.all():
#         line_total = float(item.proizvod.cena) * item.kolicina_proizvoda
#         new_total += line_total
#         item.total = line_total
#         suma       += item.total
#     # item.save()

#     # print("Suma je", suma)
#     # item.totalukupno = suma
#     # formatirano = round(suma)
#     # item.totalukupno = formatirano
#     item.save()
#     # print("Suma je", formatirano)
#     # print("Item total ukupno je", item.totalukupno)
#     postarina = 250
#     for item in Placanje.objects.all():
#         item.ukupno_bez_postarine = suma
#         sa_postarinom = suma + postarina
#         item.ukupno_sa_postarinom = sa_postarinom
#     item.save()



def checkout(request):
    placanje_obj, placanje_kreirano = Placanje.objects.id_kreiranje(request) #identicno kao i za placanje, uzimamo object tj proizvode koji su dodati na karticu
    placanje_narudzbina_obj = None #ako je nova kartica onda je narudzbina object none tj nema u bazi objekat u modelu narudzbina, nije jos kreirano. ali ako nije nova narudzbina onda je moramo kreirati iospo
    if placanje_kreirano: #ako nije nova kartica, tj ako je kartica koja je vec kreirana onda samo preusmerimo usera na home stranicu kartice
        return redirect("placanje:pocetna")
    else:
        placanje_narudzbina_obj, narudzbina_obj = Porudzbina.objects.get_or_create(placanje_narudzbina=placanje_obj) #ovaj model get or create je ugradjen u django

        for item in Placanje.objects.all():
            suma = item.ukupno_bez_postarine
            sa_postarinom = item.ukupno_sa_postarinom 
       
        for item in Porudzbina.objects.all():
            item.ukupno_bez_postarine = suma
            item.ukupno_sa_postarinom = sa_postarinom
            item.save()
            
    context = {
        'placanja': placanje_narudzbina_obj
    }
    
    return render(request, 'placanja/checkout.html', context)


def slanje_maila(request):
    placanje_obj, placanje_kreirano = Placanje.objects.id_kreiranje(request)
    placanje_narudzbina_obj, narudzbina_obj = Porudzbina.objects.get_or_create(placanje_narudzbina=placanje_obj)
    form    = Checkout_Pouzece(request.POST or None)
    if form.is_valid():
        subject = "Poruka od {}".format(form.cleaned_data['ime'])
        id_porudzbine = str(placanje_narudzbina_obj)
        message = 'Porudzbina broj: ' + id_porudzbine 
        sender  = form.cleaned_data['email']
        recipients = ['kojot841@gmail.com'] 
        try:
            send_mail(subject, message, sender, recipients, fail_silently=False)
            messages.success(request, "Porudžbina je uspešno poslata. Kontaktiraćemo Vas u najkraćem roku. Hvala Vam.")
            del request.session['placanje_id']
        except:
            pass
    context = { 
        "form": form,}

    return render(request, "placanja/checkout_done.html", context)