from django import forms
from .models import Especie


# ===============================================================
# FORMULARIO: EspecieForm
#
# Este formulario administra:
#   - Creación de especies
#   - Edición de especies
#
# Se basa en ModelForm, lo que permite:
#   - Generar automáticamente los campos según el modelo Especie
#   - Heredar validaciones y tipos declarados en el modelo
#   - Facilitar la integración con las vistas CRUD
#
# Se utiliza en las vistas:
#   - especie_crear
#   - especie_editar
#
# Campos incluidos:
#   • nombre                  → nombre único de la especie
#   • descripcion             → detalle opcional
#   • proporcion_conversion   → proporción húmedo→seco (Decimal)
#
# NOTA:
#   Validaciones adicionales (como unicidad) se manejan directamente
#   por el modelo Especie, y Django las propaga automáticamente
#   hacia este formulario.
# ===============================================================
class EspecieForm(forms.ModelForm):

    class Meta:
        # Modelo base del formulario
        model = Especie

        # Campos habilitados para edición
        fields = [
            "nombre",               # Nombre único de la especie
            "descripcion",          # Descripción opcional
            "proporcion_conversion" # Proporción húmedo→seco
        ]