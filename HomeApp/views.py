# ===============================================================
# HomeApp/views.py
#
# Módulo encargado de generar y procesar toda la lógica del
# Dashboard Ejecutivo:
#
#   - Cálculo de KPIs principales
#   - Cálculo de variaciones porcentuales
#   - Inventario actual (entradas - salidas)
#   - Cumplimiento contractual
#   - Producción mensual
#   - Ingresos proyectados
#   - Proyecciones (MySQL vs MongoDB)
#   - Distribución de inventario (pie chart)
#   - Alertas tempranas
#
# Este módulo combina datos desde:
#   * MySQL (Django ORM)
#   * MongoDB (Proyecciones)
#   * Microservicio FastAPI
#
# Todas las vistas del dashboard requieren permisos vía:
#   @requiere_permiso("PermisoVerDashboard")
# ===============================================================

from datetime import date
import calendar
import json
from decimal import Decimal

from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render

from ContratoApp.models import Contrato, EntregaContrato
from StockApp.models import Maxisaco
from EspecieApp.models import Especie
from ProyeccionesApp.services import obtener_proyecciones_por_mes


# ===============================================================
# FUNCIÓN AUXILIAR — calcular_variacion(actual, previo)
#
# Calcula la variación porcentual entre actual y previo:
#
#       ((actual - previo) / previo) * 100
#
# Se usa para mostrar KPIs con flechas ↑ / ↓ en el dashboard.
# ===============================================================
def calcular_variacion(actual, previo):
    if previo == 0:
        return 0
    return round(((actual - previo) / previo) * 100, 2)


# ===============================================================
# INVENTARIO ACTUAL — entradas - salidas por especie
#
# Se calcula:
#   - Entradas de Maxisaco
#   - Salidas de Maxisaco
#   - Inventario neto por especie
#   - Inventario total general
#
# Retorna:
#   inventario_total (Decimal)
#   inventario_especies (lista de dicts con nombre/cantidad/unidad)
# ===============================================================
def _get_inventario_actual():
    # Entradas por especie
    entradas = (
        Maxisaco.objects.filter(tipo_movimiento="entrada")
        .values("especie")
        .annotate(total=Sum("peso_kg"))
    )

    # Salidas por especie
    salidas = (
        Maxisaco.objects.filter(tipo_movimiento="salida")
        .values("especie")
        .annotate(total=Sum("peso_kg"))
    )

    # Convertir QS a diccionarios { especie_id: total }
    entradas_dict = {e["especie"]: e["total"] for e in entradas}
    salidas_dict = {s["especie"]: s["total"] for s in salidas}

    especies = Especie.objects.all()
    inventario_especies = []
    inventario_total = Decimal("0")

    # Calcular inventario neto especie por especie
    for esp in especies:
        ent = entradas_dict.get(esp.id, 0)
        sal = salidas_dict.get(esp.id, 0)

        neto = Decimal(ent or 0) - Decimal(sal or 0)
        if neto < 0:
            neto = Decimal("0")  # evitar inventario negativo

        inventario_total += neto

        inventario_especies.append(
            {
                "id": esp.id,
                "nombre": esp.nombre,
                "cantidad": float(neto),
                "unidad": "kg",
            }
        )

    return inventario_total, inventario_especies


# ===============================================================
# CUMPLIMIENTO CONTRACTUAL
#
# Calcula:
#   - toneladas requeridas
#   - toneladas cumplidas
#   - % de cumplimiento
#
# Usa agregaciones directas sobre EntregaContrato.
# ===============================================================
def _get_cumplimiento_contractual():
    datos = EntregaContrato.objects.aggregate(
        requerido=Sum("toneladas_requeridas"),
        cumplido=Sum("toneladas_cumplidas"),
    )

    requerido = Decimal(datos["requerido"] or 0)
    cumplido = Decimal(datos["cumplido"] or 0)

    if requerido == 0:
        return 0, requerido, cumplido

    cumplimiento = (cumplido / requerido) * 100
    return float(round(cumplimiento, 2)), requerido, cumplido


# ===============================================================
# PRODUCCIÓN MENSUAL DEL MES ACTUAL
#
# Consulta Maxisaco (solo entradas) entre:
#   - Primer día del mes actual
#   - Primer día del mes siguiente
#
# Retorna toneladas procesadas este mes.
# ===============================================================
def _get_produccion_mensual_actual():
    hoy = date.today()
    primer_dia = date(hoy.year, hoy.month, 1)
    prox_mes = date(hoy.year + (hoy.month == 12), (hoy.month % 12) + 1, 1)

    total_mes = (
        Maxisaco.objects.filter(
            tipo_movimiento="entrada",
            fecha_registro__gte=primer_dia,
            fecha_registro__lt=prox_mes,
        ).aggregate(total=Sum("peso_kg"))["total"]
        or 0
    )

    return float(total_mes)


# ===============================================================
# INGRESOS PROYECTADOS
#
# Basados en:
#   - contratos activos
#   - tonelaje_total acumulado
#   - precio promedio fijo (450.000 CLP/Ton)
#
# ---------------------------------------------------------------
def _get_ingresos_proyectados():
    contratos = Contrato.objects.filter(estado="activo")
    tonelaje = Decimal(contratos.aggregate(total=Sum("tonelaje_total"))["total"] or 0)
    precio_promedio = Decimal("450000")
    return float(tonelaje * precio_promedio)


# ===============================================================
# PROYECCIÓN VS CONTRACTUAL (MES A MES)
#
# Combina datos de MySQL y MongoDB:
#
#   * Contractual: toneladas requeridas (MySQL)
#   * Real: toneladas cumplidas (MySQL)
#   * Proyectado: derivado desde Mongo (microservicio FastAPI)
#
# Devuelve un diccionario listo para Chart.js:
#   {
#     labels: [...],
#     contractual: [...],
#     real: [...],
#     proyectado: [...],
#   }
# ===============================================================
def _get_proyeccion_vs_contractual():
    entregas = (
        EntregaContrato.objects.annotate(mes_int=TruncMonth("mes"))
        .values("mes_int")
        .annotate(
            contractual=Sum("toneladas_requeridas"),
            real=Sum("toneladas_cumplidas"),
        )
        .order_by("mes_int")
    )

    # Convertir QS a dict {mes: {contractual, real}}
    mysql_data = {}
    for row in entregas:
        if row["mes_int"]:
            mes = row["mes_int"].month
            mysql_data[mes] = {
                "contractual": float(row["contractual"] or 0),
                "real": float(row["real"] or 0),
            }

    # Obtener proyecciones desde Mongo
    try:
        mongo_proy = obtener_proyecciones_por_mes()
    except:
        mongo_proy = {}

    labels, contractual, real, proyectado = [], [], [], []

    # Construir arrays mes a mes
    for mes in range(1, 13):
        labels.append(calendar.month_abbr[mes])
        contractual.append(mysql_data.get(mes, {}).get("contractual", 0))
        real.append(mysql_data.get(mes, {}).get("real", 0))
        proyectado.append(mongo_proy.get(mes, contractual[-1]))

    return {
        "labels": labels,
        "contractual": contractual,
        "real": real,
        "proyectado": proyectado,
    }


# ===============================================================
# DISTRIBUCIÓN DE INVENTARIO (pie chart)
#
# Convierte cantidades en porcentajes:
#   cantidad_especie / total_inventario * 100
#
# Retorna:
#   - labels  (nombres de especies)
#   - data    (porcentajes)
# ===============================================================
def _get_distribucion_inventario(inventario_especies, inventario_total):
    if inventario_total <= 0:
        return [], []

    labels, data = [], []
    total = float(inventario_total)

    for item in inventario_especies:
        if item["cantidad"] > 0:
            labels.append(item["nombre"])
            porcentaje = (item["cantidad"] / total) * 100
            data.append(round(porcentaje, 2))

    return labels, data


# ===============================================================
# ALERTAS TEMPRANAS
#
# Genera alertas según:
#   - cumplimiento contractual bajo
#   - inventario total crítico
#
# Retorna lista de dicts con:
#   {
#      "nivel": ("alto" | "medio" | "bajo"),
#      "titulo": str,
#      "detalle": str
#   }
# ===============================================================
def _get_alertas_tempranas(cumplimiento, insumos_bajos, inventario_total):
    alertas = []

    if cumplimiento < 95:
        alertas.append(
            {
                "nivel": "alto",
                "titulo": "Riesgo de incumplimiento contractual",
                "detalle": f"Cumplimiento actual: {cumplimiento}%",
            }
        )

    if inventario_total <= 0:
        alertas.append(
            {
                "nivel": "medio",
                "titulo": "Inventario total en 0",
                "detalle": "Sin registros de stock en bodega.",
            }
        )

    return alertas


# ===============================================================
# VISTA PRINCIPAL — DASHBOARD EJECUTIVO
#
# Decorador:
#   @requiere_permiso("PermisoVerDashboard")
#
# Ensambla todo el contexto final que se envía al template:
#   dashboard/television.html
#
# Incluye:
#   - KPIs
#   - Variaciones
#   - Proyecciones (chart)
#   - Inventario (lista + pie chart)
#   - Alertas
# ===============================================================
from RolApp.decorators import requiere_permiso

@requiere_permiso("PermisoVerDashboard")
def dashboard_ejecutivo(request):

    # ----- KPIs PRINCIPALES -----
    cumplimiento, req, cum = _get_cumplimiento_contractual()
    produccion_mensual = _get_produccion_mensual_actual()
    inventario_total, inventario_especies = _get_inventario_actual()
    ingresos_proyectados = _get_ingresos_proyectados()

    # ----- VARIACIONES -----
    cumplimiento_var = calcular_variacion(cumplimiento, 98)
    produccion_var = calcular_variacion(produccion_mensual, produccion_mensual * 0.92)
    inventario_var = calcular_variacion(float(inventario_total), float(inventario_total) * 0.97)
    ingresos_var = calcular_variacion(ingresos_proyectados, ingresos_proyectados * 0.90)

    # ----- PROYECCIONES (MySQL + MongoDB) -----
    proy_vs_contractual = _get_proyeccion_vs_contractual()

    # ----- PIE INVENTARIO -----
    labels_inv, data_inv = _get_distribucion_inventario(inventario_especies, inventario_total)

    # ----- ALERTAS -----
    alertas = _get_alertas_tempranas(
        cumplimiento=cumplimiento,
        insumos_bajos=[],
        inventario_total=inventario_total,
    )

    contexto = {
        "usuario": request.user,

        # KPIs
        "cumplimiento_contractual": cumplimiento,
        "produccion_mensual": produccion_mensual,
        "inventio_total": float(inventario_total),
        "ingresos_proyectados": ingresos_proyectados,

        # Variaciones
        "cumplimiento_var": cumplimiento_var,
        "produccion_var": produccion_var,
        "inventario_var": inventario_var,
        "ingresos_var": ingresos_var,

        # Gráficos
        "chart_proy_vs_contractual": json.dumps(proy_vs_contractual),
        "chart_inv_labels": json.dumps(labels_inv),
        "chart_inv_data": json.dumps(data_inv),

        # Inventario + alertas
        "inventario_especies": inventario_especies,
        "alertas": alertas,
    }

    return render(request, "dashboard/television.html", contexto)
