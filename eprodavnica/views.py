from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.shortcuts import render
from django.views.generic import ListView
from .forms import ContactForm
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages


def about_page(request):
    return render(request, "homepage.html", {})

def contact_page(request):
    contact_form    = ContactForm(request.POST or None)
    if contact_form.is_valid():
        subject = "Poruka od {}".format(contact_form.cleaned_data['ime'])
        message = contact_form.cleaned_data['poruka']
        sender  = contact_form.cleaned_data['email']
        recipients = ['kojot841@gmail.com'] 
        try:
            send_mail(subject, message, sender, recipients, fail_silently=False)
            messages.success(request, "Poruka je uspešno poslata. Hvala Vam.")
        except:
            pass
    context = { 
        "form": contact_form,}

    return render(request, "contact.html", context)
