from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, EditProfileForm, ChangePassword
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.contrib import messages



app_name = 'registracija'

# Create your views here.
def login_page(request):
    form          = LoginForm(request.POST or None)
    context       = {
                  "form": form
                    }
    if form.is_valid():
        username   = form.cleaned_data.get("username")
        password   = form.cleaned_data.get("password")
        user       = authenticate(request, username=username, password=password)
        if user is not None:
            request.session.set_expiry(600)
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Greška prilikom logovanja. Pokušajte ponovo.")
    return render(request, "registracija/login.html", context)


User = get_user_model()

def logout_page(request):
    logout(request)
    return render(request, 'registracija/logout.html', {})


class RegisterView(FormView):
    form_class      = RegisterForm
    template_name   = 'registracija/register.html'
    success_url     = '/proizvodi/'

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(self.success_url)


@login_required
def edit_profile(request):
    print(request.method)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Uspešno ste izmenili podatke')
            return redirect('azuriranje_profila')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form':form}
        return render(request, 'registracija/edit_profile.html', args)



def change_password(request):
    if request.method == 'POST':
        form = ChangePassword(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Uspešno ste promenili lozinku!')
            update_session_auth_hash(request, form.user)
            return redirect('/')
        # else:
        #     return redirect ('accounts:password_reset_form')
    else:
        form = ChangePassword(user=request.user)
    args = {'form': form}
    return render(request, 'registracija/promena_lozinke/password_reset_form.html', args)
        