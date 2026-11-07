
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistroForm(UserCreationForm):

    first_name = forms.CharField(
        label='Nombre',
        max_length=150,
        required=True
    )

    last_name = forms.CharField(
        label='Apellido',
        max_length=150,
        required=True
    )

    email = forms.EmailField(
        label='Correo electrónico',
        required=True
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

        labels = {
            'username': 'Nombre de usuario',
        }


from .models import Tarea



class TareaForm(forms.ModelForm):

    class Meta:
        model = Tarea
        fields = [
            'titulo',
            'descripcion',
            'fecha_limite',
            'asignada_a'
        ]

        labels = {
            'titulo': 'Título de la tarea',
            'descripcion': 'Descripción',
            'fecha_limite': 'Fecha límite',
            'asignada_a': 'Asignar a empleado'
        }

        widgets = {
            'fecha_limite': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['asignada_a'].queryset = User.objects.filter(
            is_active=True,
            is_staff=False,
            is_superuser=False
        )


        labels = {
            'titulo': 'Título de la tarea',
            'descripcion': 'Descripción',
            'fecha_limite': 'Fecha límite',
            'asignada_a': 'Asignar a empleado'
        }

        widgets = {
            'fecha_limite': forms.DateInput(attrs={'type': 'date'})
        }
