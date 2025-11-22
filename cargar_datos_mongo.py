# cargar_datos_mongo.py
from pymongo import MongoClient
from datetime import datetime
import random

# ===============================================
# CONFIGURACIÓN MONGO
# ===============================================
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "proyecto_algas_db"
COLLECTION_NAME = "proyecciones"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


# ===============================================
# DATOS DE EJEMPLO
# ===============================================
especies = ["Luga Roja", "Luga Negra", "Pelillo"]

anio_actual = datetime.now().year


def generar_proyeccion_base(mes):
    """
    Genera un valor base de producción dependiendo del mes.
    Útil para que los datos se vean más reales.
    """
    if mes in (1, 2, 3):        # verano
        return random.randint(9000, 14000)
    elif mes in (4, 5, 6):      # otoño
        return random.randint(7000, 12000)
    elif mes in (7, 8, 9):      # invierno
        return random.randint(4000, 9000)
    else:                      # primavera
        return random.randint(8000, 13000)


# ===============================================
# LIMPIAR COLECCIÓN ANTES DE INSERTAR
# ===============================================
collection.delete_many({})
print("🧹 Colección 'proyecciones' limpiada.")


# ===============================================
# GENERAR DATOS
# ===============================================
documentos = []

for mes in range(1, 13):
    base = generar_proyeccion_base(mes)

    for especie in especies:
        proyeccion = base + random.randint(-500, 500)
        real = proyeccion + random.randint(-800, 800)

        doc = {
            "especie": especie,
            "anio": anio_actual,
            "mes": mes,
            "proyeccion_ton": float(proyeccion),
            "real_ton": float(max(real, 0)),
        }

        documentos.append(doc)

collection.insert_many(documentos)

print(f"✅ Se insertaron {len(documentos)} documentos en MongoDB.")
print("📌 Colección: proyecto_algas_db → proyecciones")
print("🚀 Ahora abre tu dashboard y verás los gráficos con datos reales.")
