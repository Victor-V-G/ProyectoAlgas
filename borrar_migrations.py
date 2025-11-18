import os

def eliminar_archivos_initial(directorio_base):
    """
    Recorre el directorio dado y borra todos los archivos 0001_initial.py
    que se encuentren dentro de carpetas llamadas 'migrations'.
    """
    
    # Contador para saber cuántos se borraron
    contador_borrados = 0
    
    print(f"--- Iniciando búsqueda en: {directorio_base} ---\n")

    # os.walk recorre todo el árbol de directorios
    for root, dirs, files in os.walk(directorio_base):
        
        # Verificamos si estamos dentro de una carpeta 'migrations'
        # y nos aseguramos de que NO sea dentro de site-packages o librerías externas (por seguridad)
        if 'migrations' in root and 'site-packages' not in root:
            
            target_file = "0001_initial.py"
            
            if target_file in files:
                ruta_completa = os.path.join(root, target_file)
                
                try:
                    os.remove(ruta_completa)
                    print(f"[ELIMINADO] {ruta_completa}")
                    contador_borrados += 1
                except Exception as e:
                    print(f"[ERROR] No se pudo eliminar {ruta_completa}. Razón: {e}")

    print(f"\n------------------------------------------------")
    print(f"Proceso finalizado. Total de archivos eliminados: {contador_borrados}")
    print(f"------------------------------------------------")

if __name__ == "__main__":
    # NOTA: Usa r'' antes de la ruta para evitar problemas con las barras invertidas de Windows
    ruta_proyecto = r"D:\DJANGO-APP\ProyectoAlgas"
    
    if os.path.exists(ruta_proyecto):
        eliminar_archivos_initial(ruta_proyecto)
    else:
        print(f"Error: La ruta {ruta_proyecto} no existe.")