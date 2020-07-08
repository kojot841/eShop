
<script>
 $(document).ready(function(){
   //Auto search opcija
   var pretragaForm = $(".pretraga-form") //selektor
   var pretragaInput = pretragaForm.find("[name='q']") // trazi u formi deo gde stoji name='q', u mom slucaju je to input
   var typingTimer;  //
   var vremeokidac = 1000   // 1 sekund, za koliko ce vremena da se pokrene search
   var pretragaKruzic = pretragaForm.find('[type="submit"]') // da nadje prvo submit dugme, kako bi dodao efekat tokom pretrage
   
   pretragaInput.keyup(function(event){
     clearTimeout(typingTimer) //svaki put kada 
     typingTimer = setTimeout(pretraga, vremeokidac)
   })

 function kruzicPretraga(){
   pretragaKruzic.addClass('disabled')
   pretragaKruzic.html("<i class='fa fa-spin fa-spinner'></i> Pretraga...")
 }

 function pretraga(){
   kruzicPretraga()
   var query = pretragaInput.val() //uzmi vrednost koju je user uneo, po kljucu uzima ono sto je korisnik uneo
   setTimeout(function(){
     window.location.href='/pretraga/?q=' + query
   }, 500)
 }})


 $(document).ready(function(){
   //Auto search opcija
   var pretragaForm = $(".recepti-form") //selektor
   var pretragaInput = pretragaForm.find("[name='q']") // trazi u formi deo gde stoji name='q', u mom slucaju je to input
   var typingTimer;  //
   var vremeokidac = 1000   // 1 sekund, za koliko ce vremena da se pokrene search
   var pretragaKruzic = pretragaForm.find('[type="submit"]') // da nadje prvo submit dugme, kako bi dodao efekat tokom pretrage

   
   pretragaInput.keyup(function(event){
     clearTimeout(typingTimer) //svaki put kada 
     typingTimer = setTimeout(pretraga, vremeokidac)
   })


 function kruzicPretraga(){
   pretragaKruzic.addClass('disabled')
   pretragaKruzic.html("<i class='fa fa-spin fa-spinner'></i> Pretraga...")
 }

 function pretraga(){
   kruzicPretraga()
   var query = pretragaInput.val() //uzmi vrednost koju je user uneo, po kljucu uzima ono sto je korisnik uneo
   setTimeout(function(){
     window.location.href='/pretraga_recepti/?q=' + query
   }, 500)
 }})
</script>


