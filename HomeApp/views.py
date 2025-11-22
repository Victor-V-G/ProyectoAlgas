from datetime import date
import calendar
import json
from decimal import Decimal

from django.conf import settings
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from django.shortcuts import render

from ContratoApp.models import Contrato, EntregaContrato
from StockApp.models import Maxisaco
from EspecieApp.models import Especie

# MongoDB opcional
try:
    from pymongo import MongoClient
except ImportError:
    MongoClient = None


# ==========================
#   INVENTARIO
# ==========================
def _get_inventario_actual():
    entradas = (
        Maxisaco.objects.filter(tipo_movimiento="entrada")
        .values("especie")
        .annotate(total=Sum("peso_kg"))
    )
    salidas = (
        Maxisaco.objects.filter(tipo_movimiento="salida")
        .values("especie")
        .annotate(total=Sum("peso_kg"))
    )

    entradas_dict = {e["especie"]: e["total"] for e in entradas}
    salidas_dict = {s["especie"]: s["total"] for s in salidas}

    especies = Especie.objects.all()
    inventario_especies = []
    inventario_total = Decimal("0")

    for esp in especies:
        ent = entradas_dict.get(esp.id, 0)
        sal = salidas_dict.get(esp.id, 0)

        neto = (ent or 0) - (sal or 0)
        if neto < 0:
            neto = 0

        inventario_total += neto

        inventario_especies.append({
            "id": esp.id,
            "nombre": esp.nombre,
            "cantidad": float(neto),
            "unidad": "kg",
        })

    return inventario_total, inventario_especies


# ==========================
#   CUMPLIMIENTO CONTRACTUAL
# ==========================
def _get_cumplimiento_contractual():
    datos = EntregaContrato.objects.aggregate(
        requerido=Sum("toneladas_requeridas"),
        cumplido=Sum("toneladas_cumplidas"),
    )

    requerido = datos["requerido"] or 0
    cumplido = datos["cumplido"] or 0

    if requerido == 0:
        return 0, requerido, cumplido

    return round((cumplido / requerido) * 100, 2), requerido, cumplido


# ==========================
#   PRODUCCIÓN MENSUAL
# ==========================
def _get_produccion_mensual_actual():
    hoy = date.today()
    primer_dia = date(hoy.year, hoy.month, 1)
    prox_mes = date(hoy.year + (hoy.month == 12), (hoy.month % 12) + 1, 1)

    total_mes = (
        Maxisaco.objects.filter(
            tipo_movimiento="entrada",
            fecha_registro__gte=primer_dia,
            fecha_registro__lt=prox_mes
        ).aggregate(total=Sum("peso_kg"))["total"] or 0
    )
    return float(total_mes)


# ==========================
#   INGRESOS PROYECTADOS
# ==========================
def _get_ingresos_proyectados():
    contratos = Contrato.objects.filter(estado="activo")
    tonelaje_total = contratos.aggregate(total=Sum("tonelaje_total"))["total"] or 0
    precio_promedio = Decimal("450000")  # CLP por tonelada
    return float(tonelaje_total * precio_promedio)


# ==========================
#   PROYECCIÓN VS CONTRACTUAL
# ==========================
def _get_proyeccion_vs_contractual():
    entregas = (
        EntregaContrato.objects
        .annotate(mes_only=TruncMonth("mes"))
        .values("mes_only")
        .annotate(
            contractual=Sum("toneladas_requeridas"),
            real=Sum("toneladas_cumplidas"),
        )
        .order_by("mes_only")
    )

    labels = []
    contractual_data = []
    real_data = []

    for row in entregas:
        m = row["mes_only"]
        if m:
            labels.append(calendar.month_abbr[m.month])
            contractual_data.append(float(row["contractual"] or 0))
            real_data.append(float(row["real"] or 0))

    proyectado_data = contractual_data[:]  # Default

    return {
        "labels": labels,
        "contractual": contractual_data,
        "real": real_data,
        "proyectado": proyectado_data,
    }


# ==========================
#   GRÁFICO PIE INVENTARIO
# ==========================
def _get_distribucion_inventario(inventario_especies, inventario_total):
    if inventario_total <= 0:
        return [], []

    labels = []
    data = []

    for item in inventario_especies:
        if item["cantidad"] > 0:
            labels.append(item["nombre"])
            porcentaje = (item["cantidad"] / float(inventario_total)) * 100
            data.append(round(porcentaje, 2))

    return labels, data


# ==========================
#   ALERTAS TEMPRANAS
# ==========================
def _get_alertas_tempranas(cumplimiento, insumos_bajos, inventario_total):
    alertas = []

    if cumplimiento < 95:
        alertas.append({
            "nivel": "alto",
            "titulo": "Riesgo de incumplimiento contractual",
            "detalle": f"Cumplimiento actual: {cumplimiento}%"
        })

    for ins in insumos_bajos:
        alertas.append({
            "nivel": "medio",
            "titulo": f"Insumo crítico bajo: {ins.nombre}",
            "detalle": f"Stock {ins.stock_actual} / mínimo {ins.stock_minimo}"
        })

    if inventario_total <= 0:
        alertas.append({
            "nivel": "medio",
            "titulo": "Inventario total en 0",
            "detalle": "Sin registros de stock en bodega."
        })

    return alertas


# ==========================
#   DASHBOARD EJECUTIVO
# ==========================
def dashboard_ejecutivo(request):
    cumplimiento, _, _ = _get_cumplimiento_contractual()
    produccion_mensual = _get_produccion_mensual_actual()
    inventario_total, inventario_especies = _get_inventario_actual()
    ingresos_proyectados = _get_ingresos_proyectados()

    # Como no tienes InsumosApp por ahora → lista vacía
    insumos_bajos = []

    proy_vs_contractual = _get_proyeccion_vs_contractual()
    labels_inv, data_inv = _get_distribucion_inventario(inventario_especies, inventario_total)

    alertas = _get_alertas_tempranas(
        cumplimiento=cumplimiento,
        insumos_bajos=insumos_bajos,
        inventario_total=inventario_total,
    )

    contexto = {
        "usuario": request.user,
        "cumplimiento_contractual": cumplimiento,
        "produccion_mensual": produccion_mensual,
        "inventario_total": float(inventario_total),
        "ingresos_proyectados": ingresos_proyectados,

        "chart_proy_vs_contractual": json.dumps(proy_vs_contractual),
        "chart_inv_labels": json.dumps(labels_inv),
        "chart_inv_data": json.dumps(data_inv),

        "inventario_especies": inventario_especies,
        "alertas": alertas,
    }

    return render(request, "dashboard/television.html", contexto)
