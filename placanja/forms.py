from django import forms


class Checkout_Pouzece(forms.Form):
    ime = forms.CharField(
            widget=forms.TextInput(
                    attrs={
                        "class": "form-control", 
                        "placeholder": "Vaše ime"
                    }
                    )
            )
    ulica = forms.CharField(
            widget=forms.TextInput(
                    attrs={
                        "class": "form-control", 
                        "placeholder": "Vaša ulica"
                    }
                    )
            )

    grad = forms.CharField(
            widget=forms.TextInput(
                    attrs={
                        "class": "form-control", 
                        "placeholder": "Vaš grad"
                    }
                    )
            )
    telefon = forms.CharField(
            widget=forms.TextInput(
                    attrs={
                        "class": "form-control", 
                        "placeholder": "Broj telefona"
                    }
                    )
            )
    email    = forms.EmailField(
            widget=forms.EmailInput(
                    attrs={
                        "class": "form-control", 
                        "placeholder": "Email adresa",
                        "id": "kontakt_email"
                    }
                    )
            )