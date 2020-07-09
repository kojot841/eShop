from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, ReadOnlyPasswordHashField, PasswordChangeForm


User = get_user_model()

class LoginForm(forms.Form):
    username        = forms.CharField(label='Email adresa', widget=forms.TextInput(attrs={"id":"login_username", "class": "form-control", 
                        "placeholder": "Unesite Email adresu"}))
    password        = forms.CharField(label='Lozinka', widget=forms.PasswordInput(attrs={"id":"login_password", "class": "form-control", 
                        "placeholder": "Unesite lozinku"}))


class RegisterForm(forms.ModelForm):
    password1       = forms.CharField(label='Lozinka', widget=forms.PasswordInput(attrs={"id":"register_pass1","class": "form-control", 
                        "placeholder": "Unesite lozinku",}))
    password2       = forms.CharField(label='Potvrda lozinke', widget=forms.PasswordInput(attrs={"id":"register_pass2", "class": "form-control", 
                        "placeholder": "Ponovo unesite lozinku",}))
    username        = forms.CharField(label='Korisničko ime', widget=forms.TextInput(attrs={"id":"register_username", "class": "form-control", 
                        "placeholder": "Unesite željeno korisničko ime",}))
    email           = forms.EmailField(label='Email adresa', widget=forms.TextInput(attrs={"id":"register_email","class": "form-control", 
                        "placeholder": "Unesite Email adresu",}))

    class Meta:
        model   = User
        fields  = ('email', 'username',)

    def clean_password2(self):
        password1   = self.cleaned_data.get("password1")
        password2   = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Lozinke se ne slažu! Pokušajte ponovo!")
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):

    password = ReadOnlyPasswordHashField(label=("Lozinka"),
        help_text=("Password ne čuvamo zbog sigurnosti, tako da ne postoji mogućnost da vidite trenutnu lozinku"
                    " za svoj proil,"
                    " ali možete promeniti lozinku koristeći link ispod."))
    email           = forms.EmailField(label='Email adresa',widget=forms.TextInput(attrs={"id":"editprofile_email", "class": "form-control", 
                        "placeholder": "Nova Email adresa"}) )
    username        = forms.CharField(label='Korisničko ime', widget=forms.TextInput(attrs={"id":"editprofile_username", "class": "form-control", 
                        "placeholder": "Novo korisničko ime"}))

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password'
        )

class ChangePassword(PasswordChangeForm):
    old_password       = forms.CharField(label='Stara Lozinka', widget=forms.PasswordInput(attrs={"id":"oldpass","class": "form-control", 
                        "placeholder": "Stara Lozinka"}))
    new_password1       = forms.CharField(label='Nova Lozinka', widget=forms.PasswordInput(attrs={"id":"newpass1","class": "form-control", 
                        "placeholder": "Nova lozinka",}))
    new_password2       = forms.CharField(label='Nova Lozinka potvrda', widget=forms.PasswordInput(attrs={"id":"newpass2","class": "form-control", 
                        "placeholder": "Nova lozinka"}))
    
