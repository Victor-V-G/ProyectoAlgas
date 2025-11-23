from django import forms
from .models import Insumo


# ===============================================================
# FORMULARIO: InsumoForm
#
# Este formulario se utiliza para:
#   - Crear nuevos insumos
#   - Editar insumos existentes
#
# Está basado en ModelForm, por lo que genera automáticamente
# los campos a partir del modelo Insumo y maneja validaciones
# básicas según los tipos definidos en el modelo.
#
# Se usa en las vistas:
#   - insumo_crear
#   - insumo_editar
#
# La auditoría de creado_por / actualizado_por se gestiona
# en las vistas, no en el formulario.
# ===============================================================
class InsumoForm(forms.ModelForm):

    class Meta:
        # Modelo asociado al formulario
        model = Insumo

        # Lista explícita de campos que serán visibles/editables
        fields = [
            "nombre",            # nombre del insumo (único)
            "descripcion",       # descripción opcional
            "cantidad",          # cantidad inicial o actual
            "unidad",            # unidad de medida
            "minimo_seguridad",  # umbral para alertas
        ]

