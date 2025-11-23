import os

# ======================================================
# CONFIGURA LA RUTA DE TU PROYECTO DJANGO
# ======================================================
RUTA_PROYECTO = r"D:\DJANGO-APP\ProyectoAlgas"
ARCHIVO_OBJETIVO = "0001_initial.py"

def borrar_iniciales(ruta_base):
    print("\n" + "="*60)
    print("🧹 LIMPIEZA DE ARCHIVOS 0001_initial.py")
    print("="*60)

    if not os.path.exists(ruta_base):
        print(f"❌ ERROR: La ruta {ruta_base} no existe.")
        return

    contador = 0

    for root, dirs, files in os.walk(ruta_base):
        # Filtrar solo carpetas de migraciones
        if "migrations" in root and "site-packages" not in root:
            if ARCHIVO_OBJETIVO in files:
                ruta_completa = os.path.join(root, ARCHIVO_OBJETIVO)
                try:
                    os.remove(ruta_completa)
                    print(f"🗑 Eliminado: {ruta_completa}")
                    contador += 1
                except Exception as e:
                    print(f"❌ Error eliminando {ruta_completa}: {e}")

    print("\n✔ Limpieza completa.")
    print(f"Total archivos eliminados: {contador}\n")


# ======================================================
# EJECUCIÓN PRINCIPAL
# ======================================================
if __name__ == "__main__":
    borrar_iniciales(RUTA_PROYECTO)
