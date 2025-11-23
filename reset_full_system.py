import os
import sys
import subprocess
import mysql.connector
from mysql.connector import errorcode
from pymongo import MongoClient
import time

# ===============================================================
# CONFIGURACIONES GLOBALES
# ===============================================================

PROYECTO_RUTA = r"D:\DJANGO-APP\ProyectoAlgas"
MICROSERVICIO_RUTA = r"D:\DJANGO-APP\ProyectoAlgas\microservicio_proyecciones"

ARCHIVO_MIG_INIT = "0001_initial.py"

# ------------------ MySQL ------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root"
}

MYSQL_NEW_DB = "proyecto-algas-db"
MYSQL_SYSTEM_DBS = {"information_schema", "mysql", "performance_schema", "sys", "phpmyadmin"}

# ------------------ Mongo ------------------
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "proyecto_algas_db"
MONGO_COLLECTION = "proyecciones"


# ===============================================================
# UTILIDADES
# ===============================================================

def ejecutar_comando(cmd):
    """Ejecuta un comando en consola."""
    print(f"\n▶ Ejecutando: {cmd}")
    proceso = subprocess.Popen(cmd, shell=True)
    proceso.wait()


# ===============================================================
# 1. INSTALAR DEPENDENCIAS
# ===============================================================

def instalar_dependencias():
    print("\n" + "="*60)
    print("1️⃣ INSTALANDO DEPENDENCIAS GLOBALMENTE")
    print("="*60)

    dependencias = [
        "django",
        "pymysql",
        "mysqlclient",
        "pymongo",
        "requests",
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "pydantic"
    ]

    for dep in dependencias:
        ejecutar_comando(f"pip install {dep}")

    print("✔ Dependencias instaladas.\n")


# ===============================================================
# 2. LIMPIEZA MIGRACIONES
# ===============================================================

def limpiar_migraciones(ruta):
    print("\n" + "="*60)
    print("2️⃣ LIMPIEZA DE ARCHIVOS DE MIGRACIÓN")
    print("="*60)

    eliminados = 0

    for root, dirs, files in os.walk(ruta):
        if "migrations" in root and "site-packages" not in root:
            if ARCHIVO_MIG_INIT in files:
                archivo = os.path.join(root, ARCHIVO_MIG_INIT)
                os.remove(archivo)
                eliminados += 1
                print(f"🗑 Eliminado -> {archivo}")

    print(f"✔ Total archivos eliminados: {eliminados}\n")


# ===============================================================
# 3. RESET MYSQL
# ===============================================================

def reset_mysql():
    print("\n" + "="*60)
    print("3️⃣ REINICIANDO MYSQL COMPLETAMENTE")
    print("="*60)

    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()

        cursor.execute("SHOW DATABASES")
        dbs = [d[0] for d in cursor]

        for db in dbs:
            if db not in MYSQL_SYSTEM_DBS:
                cursor.execute(f"DROP DATABASE `{db}`")
                print(f"🔥 Borrada DB: {db}")

        cursor.execute(
            f"CREATE DATABASE `{MYSQL_NEW_DB}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        print(f"✨ Nueva DB creada: {MYSQL_NEW_DB}")

        cursor.close()
        cnx.close()

    except Exception as e:
        print("❌ Error MySQL:", e)

    print("✔ MySQL listo.\n")


# ===============================================================
# 4. RESET MONGO
# ===============================================================

def reset_mongo():
    print("\n" + "="*60)
    print("4️⃣ REINICIANDO MONGODB")
    print("="*60)

    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]

    for col in db.list_collection_names():
        db[col].drop()
        print(f"🗑 Colección eliminada: {col}")

    db.create_collection(MONGO_COLLECTION)
    print(f"📁 Colección creada: {MONGO_COLLECTION}")

    print("✔ MongoDB listo.\n")


# ===============================================================
# 5. MIGRATIONS + RUNSERVER
# ===============================================================

def ejecutar_migraciones_y_servidor():
    print("\n" + "="*60)
    print("5️⃣ MIGRATIONS + INICIO DEL SERVIDOR DJANGO")
    print("="*60)

    os.chdir(PROYECTO_RUTA)

    ejecutar_comando("python manage.py makemigrations")
    ejecutar_comando("python manage.py migrate")

    print("\n✔ Migraciones completadas.\n")


# ===============================================================
# 6. INICIAR MICROSERVICIO FASTAPI
# ===============================================================

def iniciar_microservicio():
    print("\n" + "="*60)
    print("6️⃣ INICIANDO MICROSERVICIO FASTAPI")
    print("="*60)

    os.chdir(MICROSERVICIO_RUTA)

    print("📡 Microservicio en puerto 8001...")

    # Iniciar microservicio en otra ventana
    subprocess.Popen("start cmd /k uvicorn main:app --reload --port 8001", shell=True)

    time.sleep(2)
    print("✔ Microservicio levantado.\n")


# ===============================================================
# 7. INICIAR DJANGO
# ===============================================================

def iniciar_django():
    print("\n" + "="*60)
    print("7️⃣ INICIANDO SERVIDOR DJANGO")
    print("="*60)

    os.chdir(PROYECTO_RUTA)
    ejecutar_comando("python manage.py runserver")


# ===============================================================
# PROGRAMA PRINCIPAL
# ===============================================================

if __name__ == "__main__":
    print("\n🚀 INICIANDO REINICIO TOTAL DEL SISTEMA…\n")

    instalar_dependencias()
    limpiar_migraciones(PROYECTO_RUTA)
    reset_mysql()
    reset_mongo()
    ejecutar_migraciones_y_servidor()
    iniciar_microservicio()
    iniciar_django()
