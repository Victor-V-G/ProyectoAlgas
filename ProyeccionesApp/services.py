# ProyeccionesApp/services.py
from datetime import date
from django.conf import settings
from pymongo import MongoClient


def _get_mongo_client():
    uri = getattr(settings, "MONGO_URI", "mongodb://localhost:27017/")
    return MongoClient(uri)


def obtener_proyecciones_por_mes(anio: int | None = None) -> dict[int, float]:
    """
    Devuelve:
        { mes_int: total_proyectado_del_mes }

    Suma TODAS las especies por mes en Mongo.
    """
    if anio is None:
        anio = date.today().year

    db_name = getattr(settings, "MONGO_DB_NAME", "proyecto_algas_db")
    col_name = getattr(settings, "MONGO_COLLECTION_PROYECCIONES", "proyecciones")

    client = _get_mongo_client()
    db = client[db_name]
    col = db[col_name]

    pipeline = [
        {"$match": {"anio": anio}},
        {"$group": {"_id": "$mes", "proyeccion_total": {"$sum": "$proyeccion_ton"}}},
        {"$sort": {"_id": 1}},
    ]

    results = list(col.aggregate(pipeline))
    client.close()

    return {int(r["_id"]): float(r["proyeccion_total"]) for r in results}


# ProyeccionesApp/services.py (al final del archivo)
from django.db.models import Sum
from StockApp.models import Maxisaco
from EspecieApp.models import Especie
from ProyectoAlgas.mongo import get_mongo_connection
from .client import llamar_microservicio_proyecciones


def generar_proyecciones_automaticas(anio: int | None = None, meses_a_proyectar: int = 12):
    """
    1) Lee histórico de producción desde MySQL (Maxisaco) por especie.
    2) Llama al microservicio de proyecciones.
    3) Guarda/actualiza las proyecciones en MongoDB (colección 'proyecciones').

    Formato en MongoDB:
    {
        "especie": "Luga Roja",
        "anio": 2025,
        "mes": 2,
        "proyeccion_ton": 1234.56
    }
    """
    db = get_mongo_connection()
    col_name = getattr(settings, "MONGO_COLLECTION_PROYECCIONES", "proyecciones")
    col = db[col_name]

    # Si no se pasa año, se considera todo el histórico
    especies = Especie.objects.all()

    for esp in especies:
        # Histórico de producción por especie (solo entradas)
        qs = (
            Maxisaco.objects.filter(especie=esp, tipo_movimiento="entrada")
            .values("fecha_registro__year", "fecha_registro__month")
            .annotate(toneladas=Sum("peso_kg"))
            .order_by("fecha_registro__year", "fecha_registro__month")
        )

        historico = [
            {
                "anio": row["fecha_registro__year"],
                "mes": row["fecha_registro__month"],
                "toneladas": float(row["toneladas"] or 0),
            }
            for row in qs
            if row["toneladas"]
        ]

        if not historico:
            # Si no hay histórico, no proyectamos esta especie
            continue

        try:
            respuesta = llamar_microservicio_proyecciones(
                especie_nombre=esp.nombre,
                historico=historico,
                meses_a_proyectar=meses_a_proyectar,
            )
        except Exception as e:
            # Si falla el microservicio, simplemente seguimos con la siguiente especie
            print(f"[WARN] No se pudo llamar al microservicio para {esp.nombre}: {e}")
            continue

        proyecciones = respuesta.get("proyecciones", [])

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
                upsert=True,
            )

    print("✔ Proyecciones actualizadas en MongoDB desde el microservicio.")
