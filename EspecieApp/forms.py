from django import forms
from .models import Especie

class EspecieForm(forms.ModelForm):
    class Meta:
        model = Especie
        fields = [
            "nombre",
            "descripcion",
            "proporcion_conversion"
        ]
