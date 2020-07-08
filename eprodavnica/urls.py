"""eprodavnica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from .views import contact_page, about_page
from registracija.views import login_page, logout_page, RegisterView, edit_profile, change_password
from proizvodi.views import ProizvodiPregled, ProizvodiDetaljanPregled, Pretraga
from recepti. views import PretragaRecepti
from django.contrib.auth import views as authorization_views
from recepti.views import HomeView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ProizvodiPregled.as_view(), name='pocetna'),
    path('kontakt/', contact_page, name='kontakt'),
    path('o_nama/', about_page, name='o_nama'),
    path('recepti/', HomeView.as_view(), name='recepti'),
    path('prijava/', login_page, name='prijava'),
    path('odjava/', logout_page, name='odjava'),
    path('azuriranje_profila/', edit_profile, name='azuriranje_profila'),
    path('promena_lozinke/', change_password, name='promena_lozinke'),
    path('registracija/', RegisterView.as_view(), name='registracija'),
    path('proizvodi/', ProizvodiPregled.as_view(), name='proizvodi'),
    path('proizvodi/<int:pk>/', ProizvodiDetaljanPregled.as_view(), name='proizvodi_detalji'),
    path('pretraga/', include("proizvodi.urls", namespace='pretraga')),
    path('pretraga_recepti/', include("recepti.urls", namespace='pretraga_recepti')),
    path('placanje/', include("placanja.urls", namespace='placanje')),
    
    #Django password reset view urls:
    path('password_change/done/', authorization_views.PasswordChangeDoneView.as_view(template_name='registracija/promena_lozinke/password_reset_complete.html'), name='password_change_done'),
    path('password_change/', authorization_views.PasswordChangeView.as_view(template_name='registracija/promena_lozinke/password_reset_complete.html'), name='password_change'),
    path('password_reset/done/', authorization_views.PasswordResetCompleteView.as_view(template_name='registracija/promena_lozinke/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', authorization_views.PasswordResetConfirmView.as_view(template_name='registracija/promena_lozinke/password_reset_confirm.html'), name='password_reset_confirm'),
    path('zaboravljena_lozinka/', authorization_views.PasswordResetView.as_view(template_name='registracija/promena_lozinke/reset_password.html'), name='zaboravljena_lozinka'),
    path('reset/done/', authorization_views.PasswordResetCompleteView.as_view(template_name='registracija/promena_lozinke/password_reset_complete.html'), name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)