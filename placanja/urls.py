from django.urls import path

from .views import placanje, azuriranje_proizvoda, checkout, slanje_maila

app_name = "placanja"

urlpatterns = [
    path('', placanje, name='pocetna'),
    path('pocetna/', azuriranje_proizvoda, name='placanja'),
    path('checkout/', checkout, name='checkout'),
    path('checkout/done/', slanje_maila, name='pouzece'),
]