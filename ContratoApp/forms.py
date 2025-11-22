from django import forms
from .models import Contrato, EntregaContrato


class ContratoForm(forms.ModelForm):
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        input_formats=['%d-%m-%Y', '%Y-%m-%d']
    )

    fecha_fin = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        input_formats=['%d-%m-%Y', '%Y-%m-%d']
    )

    class Meta:
        model = Contrato
        fields = [
            "cliente",
            "tonelaje_total",
            "fecha_inicio",
            "fecha_fin",
            "estado"
        ]


class EntregaContratoForm(forms.ModelForm):
    mes = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        input_formats=['%d-%m-%Y', '%Y-%m-%d']
    )

    class Meta:
        model = EntregaContrato
        fields = [
            "mes",
            "toneladas_requeridas",
            "toneladas_cumplidas"
        ]
