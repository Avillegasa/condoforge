from django import forms
from .models import Vivienda, Mascota
from users.models import CustomUser

class ViviendaForm(forms.ModelForm):
    titular = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(tipo_habitante="titular"),
        required=False,
        empty_label="Selecciona un titular",
        label="Titular",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    habitantes = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(tipo_habitante__in=["copropietario", "menor", "dueno"]),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label="Habitantes"
    )

    class Meta:
        model = Vivienda
        fields = ['codigo', 'titular', 'habitantes']

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'tipo', 'raza', 'color', 'descripcion', 'foto']
