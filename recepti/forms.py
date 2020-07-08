from django import forms
from .models import Recept

class ReceptForm(forms.ModelForm):
    post = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': "Ovde možete napisati novi recept.",
            'id':'receptpost'
        }
    ))

    class Meta:
        model = Recept
        fields = ('post',)