from django import forms
from .models import Contrato, EntregaContrato

class ContratoForm(forms.ModelForm):
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
    class Meta:
        model = EntregaContrato
        fields = [
            "mes",
            "toneladas_requeridas",
            "toneladas_cumplidas"
        ]
