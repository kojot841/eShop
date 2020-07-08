# Projekat webprodavnica Kolačić
## [https://nebojsatutic.pythonanywhere.com](https://nebojsatutic.pythonanywhere.com)
Projekat Webprodavnica "Kolačić"<br>Nebojša Tutić<br>Python smer 2019/2020<br>profesor Vladimir Marić

<em>Ovo je dokumentacija za developere. Korisničku dokumentaciju pogledajte u delu "Korisnička dokumentacija".</em>

### Inicijalno podešavanje (settings.py)

Nakon pokretanja programa komandom "django/admin startproject eprodavnica" podešavamo settings.py file. U tom fajlu prvo definišemo gde ce se nalaziti statički fajlovi i media fajlovi "STATICFILES_DIRS" i MEDIA_ROOT. 

### About page i contact page

U delu Views.py dodajemo view About page koji vraća html stranicu "homepage.html". Ovaj view je jako jednostavan i sve sto on radi jeste da uzima request i vraća html stranicu definisanu u delu render (koji po default-u uzima 3 parametra).

Contact page je zamišljen kao forma uz pomoć koje nam korisnici mogu poslati email i kontaktirati nas. Prvo se dodaje novi fajl forms.py u koji nasledjujemo ugradjenu Django forms.Form formu kao i kao i ugradjeni get_user_model. Ova forma ima 3 polja, ime email i poruku. Za sva polja sam koristio Django ugradjene widgets uz pomoć kojih je moguće dodati polja kao što su class ili id pa onda je jako zgodno dodati bootstrap klasu u već ugrađenu Django formu kao i id uz pomoć kojeg možemo posle lako sa CSS-om manipulisati formom, što sam ja sve i uradio u ovom primeru. 

U delu views.py se definiše View koji će hendlovati ovu formu, tj. dajemo logiku formi ili šta ona terba da radi. Prvo treba importovati formu, i reći da ako je forma validna uzmi podatke iz forme, a to su ime, poruka i email. Ja sam koristio ugrađenu Django opciju za slanje mailova, paket send_mail za koji je neophodno definisati parametre: subject, message, sender kao i recipients ili kome će stići email. Da bi ova opcija radila potrebno je u settings.py definisati email provajdera, ja sam koristio sendgrip koji je besplatan. Nakon toga ulazi se u try blok gde kažem pokušaj da pošalješ poruku i takođe izbaci poruku useru da je uspešno poslato. U except delu izbaci da poruka nije poslata zbog greške. Na kraju vraćan contact.html stranicu. Ovaj deo je testiran i radi lepo, nakon što se pošalje forma, meni stiže email adresa sa svim podacima. 

U delu urls.py je potrebno definisati putanju. Prvo se importuje view from .views import "naziv funkcije". i onda se u delu PATH definiše putanja, dodaje se naziv funkcije koju smo importovali i takođe se dodaje name field pošto je function based view u mom pitanju, nije Class based view. 


## Aplikacija Registracija


Pošto Django dokumentaciji stoji da aplikacija treba da radi jednu stvar i tu stvar da radi savršeno, ali ne ništa više od toga ja sam pravio aplikaciju za svaki deo. Ova Aplikacija služi za hendlovanje authentikacije, tj registrovanje,logovanje ,editovanje profila, resetovanje pasworda kao i logout funkciju. 

### Forms.py
U delu forms.py sam importovao već ugradjen forms kao i getusermode. Takodje sam koristio već ugrađene UserChangeForm kao i za promenu passworda ReadOnlyPasswordHashField i PasswordChangeForm.

Usera sam nasledi ood ugradjenog getusermodel-a. Prva klasa je za logovanje korisnika koji uzima username i password. Druga klasa je registerform klasa, koja koja nasledjuje forms.Form i ona uzima username, email kao i password dva puta. U Meta klasi sam definisao User model i dodao polja username i email. Ovde nisam stavio paswwordzato sto password prolazi kroz metodu clean_password2 koja uzima oba pasworda iz forme i proverava da li su identicna. Takodje salje korisniku poruku ako lozinka nije ista. Metod save uzima password koji cuva u bazi kao i korisnika. 

Ispod je klasa za editovanje profila koja nasledjuje od UserChangeForm koja je ugradjena u Django. Po Django dokumentaciji password objekat uzima ugradjen ReadOnlyPasswordHashField metod koji ima label i help text, ja sam oba koristio u mom slucaju. Ispod se navodi sta sve korisnik moze da edituje, umom slucaju su tu email i username. 

Na kraju je klasa za zamenu paswroda, koristio sam već ugrađenu PasswordChangeForm klasu. Ona uzima tri parametra, stari pasword, novi kao i ponovljen novi password. 

###Views.py

Prva funkcija je za logovanje, uzima request kao i formu koja je definisana iznad. U delu context sam definisao ono sto funkcija vraca. Ukoliko je forma validna, uzmi podatke iz forme username i passwrord i uloguj usera. Logovanje se radi u delu authenticate koji uzima tri parametra, request username i password. Ukoliko user nije None tj ako postoji u bazi user onda ga uloguj login(request, user) i redirectuj na stranicu sa proizvodima (u mom slucaju). Ako je korisnik None, tj. ne postoji u bazi onda izbaci gresku tj. poruku "Greška prilikom logovanja. Pokušajte ponovo.". 

Logout funkcija uzima request i koristi već ugrađen logout funkciju kako bi se user izlogovao. Ona na kraju vraća template logout.html. 

Za registrovanje sam u ovom slucaju koristio Class based view za razliku od function based view iznad. Parametri koji su neophodni jesu forma, successurl kao i templatename. Ispod, u metodi se proverava da li je forma validna, uzimaju se podaci iz forme, cuva se u bazi i user se automatski loguje. Tako da korisnik nakon sto popuni registraciju biva automatski i ulogovan. 

Editovanje profila iznad imena ima mixin @login_required sto znaci da je neophodno da korisnik bude ulogovan kako bi mogao da pristupi delu za editovanje profila. Prilicno je isto kao i za sve ostale delove navedene do sada, importuje se forma, proverava se da li je request.method POST tj. da li je forma poslata. Forma uzima parametre instance.request.user tj. ono sto je korisnik uneo sa njegove strane je instanca koja se posle cuva u bazi. Ako je user izmenio emai ladresu onda je instace.request.email. Korisnik dobija obavestenje i onda se radi redirect. 

Promena lozinke je veoma slicna kao i editovanje profila ako ne i potpuno ista. 

Na kraju u delu urls.py treba definisati putanje. Prvo se importuju sve funkcije ili klase iz dela views pa se ispod u delu path definisu putanje.

## Aplikacija Proizvodi

Ova aplikacija sluzi za dodavanje i prikazivanje prozvoda. U mom slucaju ja sam odlucio da ovo bude shop za kolace pa sam se orijentisao na slike i opise kolaca. 
Aplikacija se kreira komandom python manage.py runapp proizvodi. Nakon toga u settings.py treba dodati naziv aplikacije u deo installed applications. 
Kad je reč o apkikaciji Proizvodi, počeo bih od modela. 

### Models.py 

Najvazniji, ili jedan od najvaznijih delova svake aplikacije je njena baza. U modelu definisemo bazu. Nasledio sam ugradjen models.Model i dodao polja u bazi naziv, opis, cena i slika. Posto sam koristio imagefield neophodno je instalirati pillow komandom pip install pillow. Mislim da su sva polja vec jasna cemu sluze. Nakon toga se definise __str__ metod koji vraca naziv proizvoda. U klasi Meta sam samo rekao da se model zove Proizvodi, posto django po defaultu sve modele naziva u mnozini i moj model bi se po defaultu zvao Proizvodis, ja sam dodao Meta klasu kako se to ne bi desilo. 

Dodao sam jos jedan metod url koji vraca reverse proizvodi detalji sto je naziv urla u delu urls.py kao i kwargs={'pk':self.pk}. Ovo zapravo znaci idi u url.py i nadji funkciju proizvodi_detalji koja u putanji ima proizvodi/<int:pk>/ ili id svakog proizvoda. To koristimo kako bi otvorili detaljan prikaz svakog proizvoda, uzimamo id iz baze i dodajemo ga u link proizvodi/1 proizvodi/2 itd. Za t osluzi deo <int:pk> integer pk gde je pk zapravo id broj proizvoda u bazi. To metod i kaze, pk je zapravo self.pk. Uz pomoc ovog metoda mozemo jednostavno kreirati for petlju za izlistavanje svih proizvoda na strani i imati jedan link koji ce otvarati proizvod u zavisnosti sta je korisnik kliknuo. Na ovaj nacin nista nije hardcodovano, sve je dinamicki uradjeno. Ispod cemo detalnno ovo objasniti. 


Klasa ProizvodiMenadzer uzima proizvod po id-u. Funkcija get_queryset() je vec ugradjena i ona se moze pozvati nad bazom i onda filtriramo po id-u .filter(id=id). Tako smo uzeli porizvod iz baze, ako je recimo id broj 1 uzimamo proizvod gde je id=1 ili ti prvi proizvod iz baze. Ako je broj porizvoda sa tim idjem jedan onda vrati taj proizvod return queryset.first(). Ukoliko je queryset recimo nula, prizvod vise nije u bazi onda vrati None. 
U zadnjem delu definisemo objekte tj. proizvode  objects = ProizvodiMenadzer().


Svaki put nakon kreiranja ili promene modela mora se uraditi migracija baze komandama python manage.py makemigrations i python manage.py migrate.

### Views.py

U ovom slucaju sam koristio samo Class based views. Prvi je ProizvodiPregled koji nasledjuje ListView. Ovde je quersyset su svi proizvodi u bazi i template name proizvodi.html. 

Ovde sam implementirao i pretragu. Takodje koristi ListView i i metod get_queryset. Ovaj metod uzima request kao i queryset iz forme request.GET.get('q'). Forma ima deo name='q' i ovde uzimamo taj q i onda radimo lookup uz pomoc djangovog modela Q koji smo importovali. U mom slucaju sam koristio __icontains koji trazi bilo koji deo, tj. trazi  u bzai da sadrzi tu rec. Na kraju sam pozvao .distinct() koji kaze ako search vrati dva ista proizvoda jer moze da se desi jedan isti prozivod odgovara razlicitim parametrima recimo ime i opis, onda nemoj jedan isti da prikazes dva puta vec ga samo jednom prikazi. 


## Aplikacija Placanja

Ova aplikacija sluzi za dodavanje proizvoda na karticu i dalje za placanje. Ona obavlja kompletan deo dodavanja proizvoda za placanje kao i samo placanje. 

### Models.py

Placanje model ima nekoliko polja, user koji uzima korisnika iz baze i ta veza je foreign key, proizvodi koja takdoje uzima Proizvod model iz aplikacije proizvodi i ta veza je many2many, ostala polja su: ukupno, postarina, ukupno sa postarinom i vreme. 

Placanje model uzima sesiju, tj. uzima se id placanja iz sesije request.session.get() tj. broj koji je povezan sa objektom u bazi (models-id), ako ga nemamo onda uzmi None. Onda ako imamo ID proveri da li postoji u bazi. U model menadzeru mozemo da radmo .get_queryset() a to je isto kao sto smo uradili Placanje.objects.filter. 
Ukoliko u bazi vec postoji id sa istim brojem, onda tom placanju dodeli taj id if id.count()==1:  novi_id=False placanje_obj = id.first() User krene da kupuje kao gost (nije ulogovan) doda proizvode na karticu i nakon toga se uloguje. Svi proizvodi koje je dodao kao gost ce biti sacuvani i kada se bude ulogovao. tj. sesija ili id sesije ce biti povezan sa njegovim profilom u bazi. To radi ovaj deo:  placanje_obj.user = request.user placanje_obj.save().

Ako ID ne postoji ili nije 1 (ima ih vise za isto placanje) onda kreiraj novi i dodeli sesiji, novi_id=Tru request.session['placanje_id'] = placanje_obj.id i vrati na kraju placanje objekat. 

Ispod je metod novi_id koji kreira novi id placanja ako user nije ulogovan ,ako je ulogovan onda nece kreirati novi id. 

Za racunanje ukupne cifre sam koristio signale. Ovo je moglo da se takodje izracuna u views cime bi koristili zapravo isti kod za racunanje samo bi na kraju rekli ukupno.save() ali posto sam se odlucio da koristim signale nije potrebno govoriti ukupno.save() posto signal to radi za nas. 
U presave signal delu sam uzeo sve parametre po Django dokumentaciji sender, instance, action, *args, **kwargs. Posto smo u modelu koristili Many@Many vezu onda i signal mora biti M2M i po Django dokumentaciji signal M2M uzima action parametar koji vraca nekoliko metoda, jedni od metoda su pre_remove, pre_add, kao i post_add i post_remove. Ja sam rekao ako je action jednako bilo koji od ovih metoda, onda ce signal d ase aktivira. To jeste, svaki put kada dodamo proizvod na karticu ili ga uklonimo nama je action ili post ili pre save/remove. Zbog toga bi te akcije dale signal ovom modelu  da se aktivira. Onda se ulazi i radi se racunanje koje se cuva u bazi sa instance.save(). 

m2m_changed.connect je deo koji je obavezan po Django dokumentaiji i kada se koristi m2m signal sender je naziv klase, naziv m2m fields (proizvodi) i na kraju rec through. 

Ispod racunamo postarinu i koristimo pre-save signal koji se aktivira pre nego sto se nesto sacuva u bazi. Postarinu racunamo samo ako se nalaze proizvodi u kartici, tj. ukoliko je cifra ukupno veca od nule jer nema smisla da ako je kartica prazna mi prikazemo da je cena postarice 200 dinara. Zbog toga se postarina racuna i cuva u bazi ako ako je ukpna cifra veca od nula. 


### Forms.py

U delu forms.py sam kreirao formu koju koristim nakon placanja. tj. ova forma se prikazuje ako korisnik odabere da zeli da plati pouzecem. Polja koja uzimam su ime, ulica, grad, telefon i email. Forma se ne razlikuje od kontakt forme koja je vec objasnjena iznad.


### Views.py

Prva funkcija je placanje. Prvo se prodje kroz bazu komandom Placanje.objects.id_kreiranje(request) gde je id_kreiranje metod definisam u models.py. Na kraju vracamo objekat placanja. Ovde smo objektu placanja dodeli novi id iz sesije ako juser nije ulogovan ili ako je ulogovan onda smo samo id sesije povezali sa tim userom. Ovako user moze dodati proizvode na karticu i onda posle nekoliko nedelja se ulogovati i svi proizvodi ce i dalje biti tu. 

Azuriranje proizvoda koristimo da dodajemo ili ukljanjamo proizvode sa kartice. Sakriveni deo html forme nam vraca id_proizvoda svaki put kada kliknemo da dodamo na karticu proizvod i onda taj ID proizvoda mozemo uzeti id_proizvoda = request.POST.get('id_proizvoda'). U try bloku kazem probaj da uzmes taj proizvod ako ga ima tj ako nije None. Ako je None onda korisnika vrati na stranicu placanja sa redirect, ali ako nije None onda placanje objekat dodeli id broj sesije. Ukoliko je proizvod u placanje_obj.proizvodi.all() tj ako se nalazi u korpi dodaj proizvod u many2many field tj dodaj relaciju u many2many field izmedju instance i proizvoda. 

Checkout funkcija sluzi kada korisnik doda proivode na karticu i klikni na nexr dugme, onda se pali ova funkcija koja kaze, uzmi sve proizvode koji su dodati na karticu. Ako je nova kartica onda je narudzbina object none tj nema u bazi objekat u modelu narudzbina, nije jos kreirano. ali ako nije nova narudzbina onda je moramo kreirati u else delu. 

Slanje maila sluzi kao poslednji korak, ako je korisnik odabrao posalji robu pouzecem. Jako je slican kao funkcija iznad, uzima id porudzbine, tj placanje objekat iz baze i onda uz pomoc ugradjene opcije send email koja je vec objasnjena iznad se salje email, tj nakon sto korisnik popuni narudzbinu nama stize email sa id brojem te pordzbine uz pomoc kojeg mozemo lako videti koje je sve proizvode korisnik kupio i koliko je platio. Nakon toga se brise sesija del request.session['placanje_id'] cime se svi proizvodi iz kartice brise i kartica biva prazna nakon toga. Na kraju vraca checkout_done.html stranicu.

## Aplikacija Porudzbine


Aplikacija porudzbine sluzi za kreiranje porudzbine, tj nakon sto je korisnik dodao proizvode na karticu i kliknuo na next kreira se nova porudzbina. 

### Models.py

U djangu je moguce modelu u delu choices dodeliti tuple tako da se pokazuje sa Admin strane padajuci meni sto je jako zgodno ako je u pitanju porudzbina pa mi mozemo recimo promeniti status porudzbine sa kreirana na poslata i onda cak i napraviti view koji bi poslao korisniku poslao email svaki put kada porudzbina promeni status. Model porudzbina je slican dosta modelu placanja, samo sto sam ovde morao koristiti paket math, jer ukoliko ga ne koristim DJango izbacuje gresku da ne moze da sabira decimalne brojeve i float brojeve. Zbog toga se koristi deo math.fsum([placanje_ukupno, postarina_ukupno]) koji moze sabirati decimalne i float brojeve i onda ispod samo formatiramo cifru sa formatirano = format(ukupno_novo, '.2f'). Ispod je post_save signal za racunanje ukupne cifre (svi proizvodi koji su dodati na karticu). Ako neko doda proizvode na karticu pa ode na checkout, pa se vrati nazad i doda jos neki proizvod ili ukloni neki kada klikne na next ovaj signal ce ponovo izracunati ukupnu cifru. 
Na dnu je post-save signal koji kaze ako je narudzbina created tj. ako je narudzbina tek kreirana ili ako user prvi put kreira narudzbinu onda je ukupna cifra jednaka cifri iz metode dodajukupno().

U ovoj aplikaciji nemamo nikakvu funkciju u delu voews.py ili formu u delu forms.py 


## Aplikacija Recepti

Deo recepti je zamisljen kao interaktivni deo gde bi korisnici postovali svoje recepte. Video bi se tekst recepta kao i datum i vreme kada je postovano, kao i korisnicko ime. 

### Models.py

Korisnika uzimamo iz AUTH_USER_MODEL koji se nalazi u settings file-u. U modelu definisemo usera sa foreignkey vezom, ispod toga imamo polje post i kreirano koje automatski dodaje datum kada se sacuva u bazi. 

Ovaj model je jako jednostavan i to je sve sto on uzima. 

### Forms.py

Kreiramo jednu formu, tj. formu koju ce korisnici koristiti kako bi postovali recept. Koristio sam vec ugradjene Django forme. Pravi se nova klasa i koristi se CharField koji posle ima widget TextArea, kako bi polje za upis bilo vece. Takodje dodajem atribute i jedan od njih je bootstrap klasa form-control. Takodje sam dodao ID uz pomoc kojeg sam posle u CSS jos malo oblikovao formu, tj. stavio sam border, malo promenio pozadinu da ne bude cisto bele vec malo sivkasta i takodje namestio da polje bude resizible. 

### Views.py

Kao i svuda ranije, u delu views.py definisemo funkcije koje daju logiku.U ovom slucaju sam koristio Class based view i takodje sam nasledio ugradjen TemplateView. Funkcija get, prvo definisemo formu i kazemo da su postovi Recept.objects.all().order_by('-kreirano'). Ovo je klasicna SQL komanda, prodji kroz bazu i uzmi sve objekte iz dela Recept i takodje ih sortiraj po datumu (kreirano u modelu je datetime field) od najskorijeg (zato ima minus ispred). Users je User.objects.exclude(id=request.user.id), znaci svi useri u bazi osim onoh koji imaju id jednak request.user.id sto ce biti user koji je trenutno ulogovan i koji salje formu. Na kraju vracamo context. 
Funkcija post uzima podatke iz forme ako je forma validna, cuva u bazi podatke i vraca nas na stranicu na kojoj se nalazimo. 

Takodje sam implementirao search opciju koja je slicna search opciji za pretragu proizvoda, samo sto ova search opcija sluzi za pretragu recepata. Uzima request, kao i quearyset iz forme, deo forme gde stoji name='q' i onda kazemo ako queryset nije None odradi search uz pomoc Django Q lookup-a, takodje sam koristio __icontains kao i ranije tj. ako sadrzi trazenu rec. Onda samo vracamo taj lookup ili None. Takodje sam koristio distinct() tj. ako u bazi nadje jedan objekat koji zadovoljava dva ili vise kriterijuma pretrage, nemoj onda taj jedan isti prikazivati vise puta vec samo jedan. Tako je nemoguce da dobijemo duplikate u rezultatima pretrage. 


## Aplikacija Detalji za pretragu


### Models.py

U fajlu models.py sam definisao dve klase koje sluze za dve vrste pretraga. Jedna pretraga je pretraga proizvoda (klasa DetaljiPretrage) dok je druga klasa (ReceptiPretraga) za pretragu recepata na strani recepti. Ove dve klase su jako slicne, u prvoj sam definisao naziv kao i prozivod (Many2Many) field dok sam u drugom delu recept sam isto definisao kao Many2Many field i napravio relaciju sa modelom Recept. Na kraju sam vratio string naziv obe klase. Ove dve klase zapravo sluze da bih kasnije kreirao relaciju izmedju proizvoda ili recepta i neke reci koju definisem kasnije. Tako da recimo ako u delu naziv_detalji koji sam definisao u klasi DetaljiPretrage dodam rec "nebojsa" i dodam relaciju na bilo koji proizvod (u mom slucaju sam dodao brauni kolac) ako u search polje ukucamo nebojsa search ce izbaciti brauni. Ovo je jako zgodno jer mozemo dodavati tagove za search, o ovome sam vise objasnio u delu gde sam pricao o search aplikaciji. 


## Templates

### Base.html

Base.html file je osnovni html file, tj. onaj koji koriste sve ostale stranice. Sve stranice nasledjuju ovaj html file. 
Tu se nalaze linkovi ka CSS-u, Bootstrapu, JS, Jquery kao i fontawesome koji am takodje koristio. 

Na dnu dokumenta je skripta koja daje dodatnu funkcionalnost search opciji. Tj. kada se pocnemo da kucamo search se automatski aktivira posle 1.5 sekundi sa ikonicom Trazim.. i tickicem koji se vrti. To je zapravo sve JS koji kaze uz pomoc jqery selektora formu koja ima rec pretraga-form. U toj formi nadji deo pretragaForm.find("[name='q']"). Dodaj varijablu za vreme, u mom slucaju 1.5 sekundi. Ja sam koristio keyup ugradjen JS event, i onda dodelio funkciju. Pretragu radi funkcija pretraga() koja uzima vrednost koju je korisnik uzeo i onda posle settimeout dodaje tu rec u deo ?q= tj. kao da je user uneo tu rec i kliknuo na enter. 

### Contact.html

Ovaj template koristim za kontakt stranicu ukoliko korisnik zeli da nam posalje poruku. Nasledjujem base.html i ulazim u block gde kaze ukoliko postoji poruka (poruke vraca views.py) onda prodji kroz sve poruke i if forloop.first zapravo znaci prvi put kada prodjes kroz for petlju {{message.message}} ispisi poruku. Na ovaj nacim izbegavamo da se ispisuje nekoliko istih poruka vec samo jednom. Ispod ucitavamo formu i stavljamo button posalji. 

### Homepage.html

Prikazuje podatke o firmi kao sto su lokacija i radno vreme. Takodje ucitavam iframe u kojem prikazujem tacnu lokaciju uz pomoc Google mapa. 

### Meni.html

Koristio sam Bootstrap navbar koji ako se selektuje neko polje menija ono bude aktive i razlikuje se od drugih. Da bih to mogao da postignem morao sam prvo da definisem sve putanje sa {% url 'pocetna' as pocetna %} i onda je moguce koristiti if pocetna active, tj ako je putanja pocetna postavi kao active. Ispod toga sam samo dodavao {{linkove}} koji vode do zeljenih stranica i na kraju sam implementirao search bar opcijom {% include "proizvodi/pretraga-form.html"%}. Ovo je jako zgodno posto na bilo kojem delu sajta ukoliko hocete da imate search je dovoljno samo uneti taj deo include i tako dodati search opciju. 

Takodje sam koristio deo if user.is_authenticated i onda sam prikazivao jedne opcije, dok u delu else tj. ako user nije ulogovan prikazujemo druge opcije kao sto su login, register i reset password umesto change password.

### Login.html

Ova forma koristi formu koju smo definisali u delu forms.py ali u formi paragrafa i zato sam naveo (form.as_p). Takodje ukoliko view izbaci poruku onda ce useru biti prikazana ta poruka ali samo jednom. Zato imam deo if message, pa ulazimo u for petlju i onda kazemo if forloop.first ispisi poruku, tj. za prvu iteraciju ispisi message. 

### Logout.html

Ovaj html samo izbacuje poruku useru da se uspesno izlogovao. 

### Register.html

Ucitavamo formu koju smo definisali u delu forms.py i dodajemo dugme posalji. To je sve sto ovaj template ima. 

### Edit profile.html

Isto kao i template iznad, jako je jednostavan i sve sto radi jeste da prikazuje formu definisanu u delu forms.py.


### Proizvodi.html

Ovaj html prolazi kroz sve proizvode koje imamo u bazi for pteljom for proizvod in object_list. Onda sam nakon toga koristio bootstrap card prikaz i prikazivao naziv, deskripciju, cenu i sliku proizvoda. Na kraju je link detalji koji vodi do detaljnog prikaza proizvoda, ovaj deo hendluje drugi view i template. Takodje imam deo proizvod.opis|slice:":18" gde prikazujem kratak opis. KOristio sam django pipe filter i dodao broj 18 koji kaze prikazi samo prvih 18 reci opisa proizvoda a za detaljan opis korisnik moze da klikne na dugme detalji.  

### Proizvodi_detaljno.html

Ovaj template sluzi za detaljan prikaz proizvoda. Prikazuje celu sliku u punoj rezoluciji, ceo opis kao i cenu i naziv proizvoda. Takdoje, ovde se nalazi i dugme kupi koje dodaje proizvod na karticu. Takodje imam deo if slika, tj ako porizvod ima sliku onda je prikazi ali ako nema sliku onda prikazi neku default sliku. 

### Pretraga.html

Prolazimo prvo kroz sve proizvode for petljom i onda prikazujemo proizvode isto kao i u proizvodi.html. Taj deo je identican toj formi. Na pocetku imamo if request.GET.q ispisemo q, Rezultati pretrage za: {{request.GET.q}}. Tako ispisujemo ono sto je korisnik uneo u search polje. 

### Pretraga-form.html

KOristio sam bootstrap search formu, url je pretraga:query. Pretraga je naziv view-a u file-u urls.py dok je query takodje search view-a u aplikaciji pretraga. Zbog tog sam tako napisao {% url 'pretraga:query' %}, klasa ima dodatni deo pretraga-form koji sam posle koristio za JavaScript kako bih uz pomoc jquer-a pronasao taj deo forme tj. ovu formu i onda dodao animaciju kada se radi pretraga, kao tockic koji se vrti sa natpisom trazim..Ispod toga je sve klasicno, butstrap klase, dakle nema nista specificno da sam menjao za moju aplikaciju. 


### Dodavanje_proizvoda_placanje.html

U ovom template-u prvo imam if koji kaze ako je proizvod u korpi tj. if proizvodi in placanja.proizvodi.all onda prikazi dugme ukloni proizvod, u suprotnom prikazi dugme dodaj proizvod u korpu. 


### Pretraga-recepti.html

Ovaj template je identican kao i pretraga.html, jedina razlika je zapravo u nazivu klase gde sam umesto pretraga-form dodao recepti-form koji posle uz pomoc jquery nalazim i sa java skriptom dodajem animaciju trazim..

### Recepti.html

Ukoliko je korisnik ulogovan, onda dodaj search bar prvo pa ispod formu post koju sam definisao u forms.py delu. 
Ispod toga prolazim kroz sve postove u bazi sa for post in posts i ispisujem post kao i vreme,username korisnika koji je to postovao. 
U else delu na kraju kazem ako korisnik nije ulogovan onda ispisi poruku da se mora ulogovati kako bi video recepte, takodje sam tu ukljucio login link. 

### Main.css

U ovom fajlu se nalazi css za ceo sajt, posto sve stranice nasledjuju base.html u kojem se nalazi tj. u kojem sam ucitao ovaj css file. Prvo sam celom body-u dodao pozadinu tj ucitao sliku koja se nalazi u folderu static/pozadina.png. Takodje sam font prmenio da bude 500 bold i velicinu fonta sam malo povecao . Zamenio sam posle font family, stavio sam da default font bude Amatic SC', cursive, ali ako taj font nije dostupan na sistemu onda je zamenski font Sans-Serif. Deo #card-opacity znaci da sam svim karticama (kartice na kojima se ucitavaju proizvodi na stranici proizvodi) dodao logo firme, kao mali kolacic. Tu sam rekao gde slika treba da se nalazi kao i koje velicine da bude kako bi se lepo uklopila na velicinu kartice. Ispod sam onda redom izlistavao sve klase ili id-jeve kojima sam menjao uglavnom velicinu, dodavao margine, itd. U delu #receptpost sam po id promenio kako izgleda polje u koje korisnik unosi novi recept. Stavio sam default visinu, padding, backgropud boju da bude sivkasta, border i takodje da bude resizible tj da korisnik moze sam da menja velicinu prozora. 

### Media 

Folder Media koji se nalazi u folderu staticki_fajlovi sluzi da se svi media fajlovi (slike) nalaze na jednom mestu. Ovaj folder smo definisali u settings.py tj. putanju do ovog foldera tak oda aplikacija zna gde se nalaze media fajlovi. Tu su slike svih kolaca, logo kao i pozadina koju sam koristio na sajtu. Kada dodajemo novi proizvod sa admin strane, na poslednjem delu nakokn sto smo uneli naziv proizvoda, cenu i opis imamo pciju da uploadujemo sliku, tada selektujemo neku sliku koja se nakon uploada automatski pojavljuje u ovom folderu ali sa nazivom koji je jedinstven tako da ne moze da se desi da imamo dva fajla sa istim imemom. DJango model automatski menja naziv fajla tako sto mu dodaje custome brojeve i slova nakon naziva pa imamo recimo brauni_7c9yQR1... Ovo je jako zgodno jer ako imamo jako puno slika, recimo stotine slika ili ako user uploaduje slike (recimo kao na Facebook-u) postoji onda velika verovatnoca da se naziv slike poklopi sa nazivom slike koja je vec u bazi, onda django model automatski menja naziv kako bi bio jedinstven. 