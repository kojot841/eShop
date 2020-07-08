from django.urls import path

from .views import PretragaRecepti

app_name = "recepti"

urlpatterns = [
    path('', PretragaRecepti.as_view(), name='query'),
]