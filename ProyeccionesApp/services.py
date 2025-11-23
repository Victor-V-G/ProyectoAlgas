# ================================================================
# ProyeccionesApp/services.py
#
# Servicios relacionados a la generación y obtención de proyecciones.
#
# Aquí se manejan:
#   - Consultas a MongoDB
#   - Agregaciones por mes/año
#   - Lectura de histórico desde Django ORM
#   - Comunicación con microservicios externos
#   - Escritura/actualización de proyecciones en la colección Mongo
#
# Este archivo actúa como capa LÓGICA independiente de las vistas.
# ================================================================

from datetime import date
from django.conf import settings
from pymongo import MongoClient


# ================================================================
# FUNCIÓN PRIVADA: _get_mongo_client()
#
# Obtiene un cliente MongoDB utilizando la URI configurada en
# settings.py. Si la variable no existe, usa localhost por defecto.
#
# Esta función NO selecciona base de datos; solo abre conexión.
# ================================================================
def _get_mongo_client():
    uri = getattr(settings, "MONGO_URI", "mongodb://localhost:27017/")
    return MongoClient(uri)


# ================================================================
# obtener_proyecciones_por_mes()
#
# Retorna un diccionario con la suma TOTAL de proyecciones por mes:
#
#    { mes_int: total_proyectado_en_toneladas }
#
# Datos provienen EXCLUSIVAMENTE de MongoDB.
#
# Parámetros:
#   anio: año a consultar (si no se pasa → año actual)
#
# Flujo:
#   1. Selecciona BD y colección configuradas en settings.
#   2. Ejecuta un pipeline de agregación:
#        - match por año
#        - group por mes
#        - sumatoria de proyeccion_ton
#        - sort ascendente por mes
#   3. Retorna datos en un formato limpio (dict).
# ================================================================
def obtener_proyecciones_por_mes(anio: int | None = None) -> dict[int, float]:

    if anio is None:
        anio = date.today().year

    # Obtención desde settings (con valores por defecto)
    db_name = getattr(settings, "MONGO_DB_NAME", "proyecto_algas_db")
    col_name = getattr(settings, "MONGO_COLLECTION_PROYECCIONES", "proyecciones")

    # Conexión y selección de colección
    client = _get_mongo_client()
    db = client[db_name]
    col = db[col_name]

    # ------------------------------------------------------------
    # Pipeline de agregación MongoDB:
    #   $match: filtrar por año
    #   $group: sumar toneladas por mes
    #   $sort: ordenar cronológicamente
    # ------------------------------------------------------------
    pipeline = [
        {"$match": {"anio": anio}},
        {"$group": {"_id": "$mes", "proyeccion_total": {"$sum": "$proyeccion_ton"}}},
        {"$sort": {"_id": 1}},
    ]

    results = list(col.aggregate(pipeline))
    client.close()

    # Convertir a { mes_int: total_float }
    return {int(r["_id"]): float(r["proyeccion_total"]) for r in results}


# ================================================================
# IMPORTS ADICIONALES PARA GENERACIÓN AUTOMÁTICA
# (Estos deben ir al final para evitar dependencias circulares)
# ================================================================
from django.db.models import Sum
from StockApp.models import Maxisaco
from EspecieApp.models import Especie
from ProyectoAlgas.mongo import get_mongo_connection
from .client import llamar_microservicio_proyecciones


# ================================================================
# generar_proyecciones_automaticas()
#
# Función PRINCIPAL del módulo.
#
# Flujo completo:
#   1) Obtiene histórico de producción desde MySQL (Django ORM).
#      - Se agrupa por año/mes
#      - Solo se consideran entradas
#
#   2) Por cada especie → llama al microservicio de proyecciones:
#        llamar_microservicio_proyecciones()
#
#      Este microservicio retorna un array con:
#         {
#             "anio": 2025,
#             "mes": 2,
#             "proyeccion_ton": 1234.56
#         }
#
#   3) Se guardan/actualizan las proyecciones en MongoDB usando
#      update_one(..., upsert=True), lo que permite:
#        ✓ actualizar si existe
#        ✓ crear si no existe
#
#   4) Imprime un log confirmando que todo fue exitoso.
#
# Parámetros:
#   - anio: si se quiere proyectar solo un año específico (opcional)
#   - meses_a_proyectar: horizonte del microservicio
#
# ================================================================
def generar_proyecciones_automaticas(anio: int | None = None, meses_a_proyectar: int = 12):

    # Selección de base Mongo
    db = get_mongo_connection()
    col_name = getattr(settings, "MONGO_COLLECTION_PROYECCIONES", "proyecciones")
    col = db[col_name]

    # Todas las especies registradas en MySQL
    especies = Especie.objects.all()

    for esp in especies:

        # ------------------------------------------------------------
        # 1. HISTÓRICO DESDE MYSQL (Django ORM)
        #
        #   Se obtienen SOLO movimientos de tipo "entrada".
        #   Se agrupan por año y mes sumando peso total.
        # ------------------------------------------------------------
        qs = (
            Maxisaco.objects.filter(especie=esp, tipo_movimiento="entrada")
            .values("fecha_registro__year", "fecha_registro__month")
            .annotate(toneladas=Sum("peso_kg"))
            .order_by("fecha_registro__year", "fecha_registro__month")
        )

        # Convertir QuerySet a lista limpia
        historico = [
            {
                "anio": row["fecha_registro__year"],
                "mes": row["fecha_registro__month"],
                "toneladas": float(row["toneladas"] or 0),
            }
            for row in qs
            if row["toneladas"]  # excluir meses sin producción
        ]

        # Si no hay histórico → saltar especie
        if not historico:
            continue

        # ------------------------------------------------------------
        # 2. LLAMADA AL MICROSERVICIO DE PROYECCIONES
        #
        # Este microservicio recibe TODO el historial y
        # devuelve proyecciones hacia adelante.
        #
        # Si falla → se continúa con la siguiente especie.
        # ------------------------------------------------------------
        try:
            respuesta = llamar_microservicio_proyecciones(
                especie_nombre=esp.nombre,
                historico=historico,
                meses_a_proyectar=meses_a_proyectar,
            )
        except Exception as e:
            print(f"[WARN] No se pudo llamar al microservicio para {esp.nombre}: {e}")
            continue

        proyecciones = respuesta.get("proyecciones", [])

        # ------------------------------------------------------------
        # 3. GUARDAR PROYECCIONES EN MONGO
        #
        # Se utiliza:
        #   update_one(filtro, {"$set": datos}, upsert=True)
        #
        # Esto garantiza:
        #   ✓ si ya existe → se actualiza
        #   ✓ si no existe → se crea el registro
        # ------------------------------------------------------------
        for p in proyecciones:
            anio_p = int(p["anio"])
            mes_p = int(p["mes"])
            proy_ton = float(p["proyeccion_ton"])

            col.update_one(
                {
                    "especie": esp.nombre,
                    "anio": anio_p,
                    "mes": mes_p,
                },
                {
                    "$set": {
                        "especie": esp.nombre,
                        "anio": anio_p,
                        "mes": mes_p,
                        "proyeccion_ton": proy_ton,
                    }
                },
                upsert=True,  # crea si no existe
            )

    # ------------------------------------------------------------
    # 4. CONFIRMACIÓN EN CONSOLA (log)
    # ------------------------------------------------------------
    print("Proyecciones actualizadas en MongoDB desde el microservicio.")
