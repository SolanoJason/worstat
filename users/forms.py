from django import forms
from .models import Account
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms.widgets import FileInput

User = get_user_model()

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'full_name']

class UserProfileForm(forms.ModelForm):

    picture = forms.ImageField(max_length=500, allow_empty_file=False, required=False, label='Perfil', error_messages={
        'required': 'Este campo es requerido.',
        'invalid': 'No se ha enviado ningún fichero. Compruebe el tipo de codificación en el formulario.',
        'missing': 'No se envió ningún archivo.',
        'empty': 'El archivo enviado está vació.',
        'max_length': '',
        'contradiction': 'Por favor envíe un fichero o marque la casilla de limpiar, pero no ambos.',
        'invalid_image': 'Adjunte una imagen válida. El archivo adjunto o bien no es una imagen o bien está dañado.'
    }, widget=FileInput())

    class Meta:
        model = User
        fields = ['picture', 'full_name', 'about']