from django import forms
from .models import Gasolinera
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FormularioGasolinera(forms.ModelForm):
    class Meta:
        model = Gasolinera
        fields = '__all__'
        widgets = {}


class FormularioRegistro(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']