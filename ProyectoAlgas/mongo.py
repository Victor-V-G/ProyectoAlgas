from pymongo import MongoClient
from django.conf import settings


# ====================================================================
# FUNCIÓN: get_mongo_connection()
#
# Propósito:
#   - Establece y retorna una conexión a MongoDB utilizando PyMongo.
#   - Obtiene los parámetros de conexión desde settings.py
#     (si existen), de lo contrario usa valores por defecto.
#
# Uso típico:
#     db = get_mongo_connection()
#     collection = db["nombre_coleccion"]
#
# Todos los módulos que necesiten interactuar con MongoDB deben
# utilizar esta función para garantizar una conexión consistente.
# ====================================================================
def get_mongo_connection():

    # ---------------------------------------------------------------
    # 1. OBTENER URI DE CONEXIÓN
    #
    # getattr(settings, "MONGO_URI", default)
    #   → Si la variable existe en settings, la usa.
    #   → Si no, usa "mongodb://localhost:27017/" como fallback.
    #
    # Ejemplos válidos de MONGO_URI:
    #   - mongodb://localhost:27017/
    #   - mongodb://usuario:clave@host:27017/
    #   - mongodb+srv://cluster.mongodb.net/
    # ---------------------------------------------------------------
    uri = getattr(settings, "MONGO_URI", "mongodb://localhost:27017/")

    # Crear cliente de conexión a MongoDB
    client = MongoClient(uri)

    # ---------------------------------------------------------------
    # 2. OBTENER NOMBRE DE LA BASE DE DATOS
    #
    # Configurable vía settings.py:
    #    MONGO_DB_NAME = "proyecto_algas_db"
    #
    # Si no está definido → usa "proyecto_algas_db" como valor por defecto.
    # ---------------------------------------------------------------
    db_name = getattr(settings, "MONGO_DB_NAME", "proyecto_algas_db")

    # Retorna el objeto de base de datos listo para usar
    return client[db_name]
