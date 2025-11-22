# limpiar_mongo.py
from pymongo import MongoClient

# ===============================================
# CONFIGURACIÓN MONGO
# ===============================================
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "proyecto_algas_db"
COLLECTION_NAME = "proyecciones"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

print("🧹 Iniciando limpieza total de MongoDB…")

# ===============================================
# ELIMINAR TODAS LAS COLECCIONES DEL DATABASE
# ===============================================
colecciones = db.list_collection_names()

for col in colecciones:
    db[col].drop()
    print(f"🗑️ Colección eliminada: {col}")

print("✔ Todas las colecciones fueron eliminadas.")

# ===============================================
# CREAR SOLO LA COLECCIÓN proyecciones (vacía)
# ===============================================
db.create_collection(COLLECTION_NAME)
print(f"📁 Colección creada nuevamente: {COLLECTION_NAME}")

print("✅ Base limpia y lista.")
