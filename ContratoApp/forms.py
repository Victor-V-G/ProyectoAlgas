from django import forms
from django.db.models import Sum

from .models import Contrato, EntregaContrato
from EspecieApp.models import Especie
from StockApp.models import Maxisaco


# ===============================================================
# FORMULARIO: ContratoForm
# ===============================================================
class ContratoForm(forms.ModelForm):

    fecha_inicio = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"},
            format="%Y-%m-%d",
        ),
        input_formats=["%d-%m-%Y", "%Y-%m-%d"],
        label="Fecha de Inicio",
    )

    fecha_fin = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"},
            format="%Y-%m-%d",
        ),
        input_formats=["%d-%m-%Y", "%Y-%m-%d"],
        label="Fecha de Término",
    )

    class Meta:
        model = Contrato
        fields = [
            "cliente",
            "tonelaje_total",
            "fecha_inicio",
            "fecha_fin",
            "estado",
        ]

        labels = {
            "cliente": "Cliente",
            "tonelaje_total": "Kilogramos Totales (KG)",
            "estado": "Estado del Contrato",
        }


# ===============================================================
# FORMULARIO: EntregaContratoForm
# ===============================================================
class EntregaContratoForm(forms.ModelForm):

    mes = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"},
            format="%Y-%m-%d",
        ),
        input_formats=["%d-%m-%Y", "%Y-%m-%d"],
        label="Mes de Entrega",
    )

    especie = forms.ModelChoiceField(
        queryset=Especie.objects.all(),
        label="Especie de Alga",
        empty_label="Seleccione una especie",
    )

    class Meta:
        model = EntregaContrato
        fields = [
            "especie",
            "mes",
            "toneladas_requeridas",
            "toneladas_cumplidas",
        ]

        labels = {
            "toneladas_requeridas": "Kilogramos Requeridos (KG)",
            "toneladas_cumplidas": "Kilogramos Entregados (KG)",
        }


    def clean(self):
        cleaned_data = super().clean()

        especie = cleaned_data.get("especie")
        kg_requeridos = cleaned_data.get("toneladas_requeridas")
        kg_entregados = cleaned_data.get("toneladas_cumplidas")

        # -------------------------------
        # Validación base
        # -------------------------------
        if not especie or kg_requeridos is None or kg_entregados is None:
            return cleaned_data

        # -------------------------------
        # Cálculo de stock real
        # -------------------------------
        entradas = Maxisaco.objects.filter(
            especie=especie,
            tipo_movimiento="entrada",
        ).aggregate(total=Sum("peso_kg"))["total"] or 0

        salidas = Maxisaco.objects.filter(
            especie=especie,
            tipo_movimiento="salida",
        ).aggregate(total=Sum("peso_kg"))["total"] or 0

        stock_real = entradas - salidas


        if kg_requeridos > stock_real:
            self.add_error(
                "toneladas_requeridas",
                f"No hay stock suficiente para {especie.nombre}. "
                f"Stock disponible: {stock_real:.2f} KG."
            )


        if kg_entregados > kg_requeridos:
            self.add_error(
                "toneladas_cumplidas",
                "Los kilogramos entregados no pueden ser mayores a los kilogramos requeridos."
            )

        return cleaned_data


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        especies_con_stock = []

        for especie in Especie.objects.all():

            entradas = Maxisaco.objects.filter(
                especie=especie,
                tipo_movimiento="entrada"
            ).aggregate(total=Sum("peso_kg"))["total"] or 0

            salidas = Maxisaco.objects.filter(
                especie=especie,
                tipo_movimiento="salida"
            ).aggregate(total=Sum("peso_kg"))["total"] or 0

            stock = entradas - salidas

            especies_con_stock.append(
                (especie.id, f"{especie.nombre} | Stock: {stock:.2f} KG")
            )


        self.fields["especie"].choices = especies_con_stock
