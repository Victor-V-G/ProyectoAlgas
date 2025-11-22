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
