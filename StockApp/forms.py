from django import forms
from .models import Maxisaco

class MaxisacoForm(forms.ModelForm):
    class Meta:
        model = Maxisaco
        fields = [
            "especie",
            "peso_kg",
            "tipo_movimiento",
            "observaciones"
        ]
