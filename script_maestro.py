import os
import sys
import mysql.connector
from mysql.connector import errorcode

# ==========================================
# CONFIGURACIÓN GLOBAL
# ==========================================

# 1. Configuración de Archivos
# ------------------------------------------
# Asegúrate de que esta ruta sea correcta en tu máquina
RUTA_PROYECTO = r"D:\DJANGO-APP\ProyectoAlgas"
ARCHIVO_OBJETIVO = "0001_initial.py"

# 2. Configuración de Base de Datos
# ------------------------------------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',      
    'password': 'root',  # Verifica si tu contraseña es 'root' o vacía ''
}

NUEVA_DB_NOMBRE = 'proyecto-algas-db'

# Bases de datos del sistema (PROTEGIDAS - No se borrarán)
SYSTEM_DBS = {
    'information_schema', 'mysql', 'performance_schema', 'sys', 'phpmyadmin'
}

# ==========================================
# FUNCIONES
# ==========================================

def paso_1_limpiar_archivos(directorio_base):
    """Busca y elimina archivos de migración iniciales sin confirmar."""
    print("\n" + "="*60)
    print("PASO 1: LIMPIEZA DE ARCHIVOS DE MIGRACIÓN")
    print("="*60)
    
    if not os.path.exists(directorio_base):
        print(f"❌ Error: La ruta {directorio_base} no existe.")
        return

    contador_borrados = 0
    print(f"📂 Buscando en: {directorio_base}\n")

    for root, dirs, files in os.walk(directorio_base):
        # Filtro de seguridad: solo dentro de 'migrations' y fuera de libs externas
        if 'migrations' in root and 'site-packages' not in root:
            if ARCHIVO_OBJETIVO in files:
                ruta_completa = os.path.join(root, ARCHIVO_OBJETIVO)
                try:
                    os.remove(ruta_completa)
                    print(f"   🗑️ [ELIMINADO] {ruta_completa}")
                    contador_borrados += 1
                except Exception as e:
                    print(f"   ❌ [ERROR] Falló eliminar {ruta_completa}: {e}")

    print(f"\n✅ Paso 1 completado. Archivos eliminados: {contador_borrados}")


def paso_2_reset_base_datos():
    """Borra DBs de usuario y crea la nueva base de datos automáticamente."""
    print("\n" + "="*60)
    print("PASO 2: REINICIO DE BASE DE DATOS MYSQL (AUTOMÁTICO)")
    print("="*60)
    
    print(f"🔌 Conectando a MySQL en {DB_CONFIG['host']}...")

    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()
        
        # Obtener DBs
        cursor.execute("SHOW DATABASES")
        dbs_usuario = [db[0] for db in cursor if db[0] not in SYSTEM_DBS]
        
        if not dbs_usuario:
            print("ℹ️  No se encontraron bases de datos de usuario para borrar.")
        else:
            print(f"\n⚠️  Eliminando {len(dbs_usuario)} bases de datos encontradas...")
            
            # Bucle de eliminación directa (SIN CONFIRMACIÓN)
            for db in dbs_usuario:
                try:
                    cursor.execute(f"DROP DATABASE `{db}`")
                    print(f"   🔥 [BORRADA] {db}")
                except mysql.connector.Error as err:
                    print(f"   ❌ [ERROR] No se pudo borrar {db}: {err}")

        # Crear nueva DB
        print(f"\n✨ Creando nueva base de datos: {NUEVA_DB_NOMBRE}")
        try:
            cursor.execute(
                f"CREATE DATABASE `{NUEVA_DB_NOMBRE}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            print(f"   ✅ Base de datos '{NUEVA_DB_NOMBRE}' creada exitosamente.")
        except mysql.connector.Error as err:
            print(f"   ❌ Error al crear la base de datos: {err}")

        cursor.close()
        cnx.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("❌ Error de autenticación: Revisa tu usuario y contraseña en DB_CONFIG.")
        else:
            print(f"❌ Error de conexión MySQL: {err}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


# ==========================================
# EJECUCIÓN PRINCIPAL
# ==========================================

if __name__ == "__main__":
    print("INICIANDO HARD RESET AUTOMÁTICO PARA DJANGO...")
    
    # Ejecutar Paso 1
    paso_1_limpiar_archivos(RUTA_PROYECTO)
    
    # Ejecutar Paso 2
    paso_2_reset_base_datos()
    
    print("\n" + "="*60)
    print("🏁 PROCESO FINALIZADO")
    print("="*60)
    print("Siguientes pasos en consola:")
    print(">> python manage.py makemigrations")
    print(">> python manage.py migrate")