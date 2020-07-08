from django.urls import path

from .views import Pretraga

app_name = "proizvodi"

urlpatterns = [
    path('', Pretraga.as_view(), name='query'),
]