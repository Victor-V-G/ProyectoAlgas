from django import forms
from .models import Maxisaco


# ================================================================
# FORMULARIO: MaxisacoForm
#
# Formulario basado en ModelForm para crear/editar registros
# del modelo Maxisaco.
#
# Este formulario se utiliza en:
#   - stock_crear (crear nuevo maxisaco)
#   - stock_editar (editar registro existente)
#
# Permite controlar qué campos son visibles y editables
# desde la interfaz, manteniendo fuera del formulario los
# campos automáticos o manejados por el sistema:
#   - registrado_por        (asignado en la vista)
#   - actualizado_por       (asignado en la vista)
#   - fecha_registro        (auto_now_add)
#   - fecha_actualizacion   (auto_now)
# ================================================================
class MaxisacoForm(forms.ModelForm):

    class Meta:
        # Modelo asociado al formulario
        model = Maxisaco

        # ----------------------------------------------------------
        # CAMPOS INCLUIDOS EN EL FORMULARIO
        #
        # Solo estos campos aparecerán en los templates.
        # Los campos controlados por el sistema NO se muestran.
        # ----------------------------------------------------------
        fields = [
            "especie",          # FK: especie seleccionada
            "peso_kg",          # decimal: peso del maxisaco
            "tipo_movimiento",  # entrada / salida
            "observaciones"     # campo opcional
        ]
