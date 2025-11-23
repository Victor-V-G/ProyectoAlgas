from django import forms
from .models import Contrato, EntregaContrato


# ===============================================================
# FORMULARIO: ContratoForm
#
# Función:
#   Administrar la creación y edición de contratos.
#
# Características:
#   - Usa ModelForm para derivar validaciones desde el modelo.
#   - Sobrescribe fecha_inicio y fecha_fin para utilizar
#     <input type="date"> compatible con navegadores modernos.
#
# input_formats:
#   Se soportan ambos formatos:
#     • dd-mm-YYYY  (ej: 12-02-2025)
#     • YYYY-mm-dd  (formato estándar HTML5)
#
# Se utiliza en:
#   - contrato_crear
#   - contrato_editar
#
# Campos:
#   cliente
#   tonelaje_total
#   fecha_inicio
#   fecha_fin
#   estado
# ===============================================================
class ContratoForm(forms.ModelForm):

    # -----------------------------------------------------------
    # Campo: fecha_inicio
    #
    # widget=forms.DateInput(...):
    #     Renderiza un input tipo "date" HTML5
    #
    # input_formats:
    #     Acepta dos formatos para flexibilidad al ingresar datos
    # -----------------------------------------------------------
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d',
        ),
        input_formats=['%d-%m-%Y', '%Y-%m-%d'],
    )

    # -----------------------------------------------------------
    # Campo: fecha_fin
    #
    # Funciona exactamente igual que fecha_inicio,
    # asegurando compatibilidad y consistencia.
    # -----------------------------------------------------------
    fecha_fin = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d',
        ),
        input_formats=['%d-%m-%Y', '%Y-%m-%d'],
    )

    class Meta:
        model = Contrato

        # Campos habilitados para el formulario
        fields = [
            "cliente",         # Nombre del cliente
            "tonelaje_total",  # Toneladas totales comprometidas
            "fecha_inicio",    # Fecha de inicio del contrato
            "fecha_fin",       # Fecha de término
            "estado"           # Estado del contrato (activo/completado/cancelado)
        ]


# ===============================================================
# FORMULARIO: EntregaContratoForm
#
# Función:
#   Administrar la creación y edición de entregas asociadas
#   a un contrato.
#
# Widgets:
#   - Se implementa un input tipo "date" para el campo mes.
#
# Notas:
#   - Aunque es un DateField, el valor representa un *mes*,
#     normalmente usando día 1 (ej: 2025-03-01 → Marzo 2025).
#
# Utilizado en:
#   - entrega_crear
#   - entrega_editar
#
# Campos:
#   mes
#   toneladas_requeridas
#   toneladas_cumplidas
# ===============================================================
class EntregaContratoForm(forms.ModelForm):

    # -----------------------------------------------------------
    # Campo: mes
    #
    # Usado para seleccionar el mes correspondiente a la entrega.
    #
    # input_formats:
    #   Soporta tanto dd-mm-YYYY como YYYY-mm-dd.
    # -----------------------------------------------------------
    mes = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d',
        ),
        input_formats=['%d-%m-%Y', '%Y-%m-%d'],
    )

    class Meta:
        model = EntregaContrato

        fields = [
            "mes",                  # Mes de entrega (DateField)
            "toneladas_requeridas", # Cantidad planificada
            "toneladas_cumplidas",  # Cantidad efectivamente entregada
        ]
