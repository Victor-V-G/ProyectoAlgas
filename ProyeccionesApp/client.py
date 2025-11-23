# ===============================================================
# ProyeccionesApp/client.py
#
# Cliente HTTP que se comunica con el microservicio de proyecciones.
#
# Función principal:
#   llamar_microservicio_proyecciones()
#
# Este microservicio (generalmente FastAPI) recibe:
#   - nombre de especie
#   - histórico de producción mensual
#   - cantidad de meses a proyectar
#
# Y devuelve:
#   - lista de proyecciones para los meses futuros
#
# Este archivo aísla la comunicación HTTP de la lógica interna,
# facilitando mantenimiento, testing y cambios de infraestructura.
# ===============================================================

import requests
from django.conf import settings


# ===============================================================
# llamar_microservicio_proyecciones()
#
# Llama vía HTTP POST al servicio externo encargado de calcular
# proyecciones estadísticas para cada especie.
#
# Parámetros:
#   - especie_nombre (str):
#         Nombre de la especie (ej: "Luga Roja").
#
#   - historico (list[dict]):
#         Lista en formato:
#             {
#                 "anio": int,
#                 "mes": int,
#                 "toneladas": float
#             }
#
#         Este histórico es construido previamente desde MySQL usando
#         el modelo Maxisaco.
#
#   - meses_a_proyectar (int):
#         Cantidad de meses futuros que el microservicio debe proyectar.
#
# Uso:
#       respuesta = llamar_microservicio_proyecciones("Luga Roja", historico, 12)
#
# Retorna:
#       dict con estructura:
#       {
#           "proyecciones": [
#               { "anio": 2025, "mes": 2, "proyeccion_ton": 123.45 },
#               ...
#           ]
#       }
#
# Errores:
#   - raise_for_status() lanza excepción si el servidor responde con error.
#
# Configuración:
#   En settings.py puedes definir:
#       PROYECCIONES_MICRO_URL = "http://mi_microservicio/api/proyectar"
#
#   Si no existe, se usa el endpoint local por defecto.
# ===============================================================
def llamar_microservicio_proyecciones(
    especie_nombre: str,
    historico: list,
    meses_a_proyectar: int = 12
) -> dict:

    # ------------------------------------------------------------
    # URL DEL MICROSERVICIO
    #
    # Se obtiene desde settings.py para permitir flexibilidad:
    #   - ambientes dev/staging/producción
    #   - despliegue en Docker/Kubernetes
    #
    # Valor por defecto: API FastAPI corriendo en localhost:8001.
    # ------------------------------------------------------------
    url = getattr(
        settings,
        "PROYECCIONES_MICRO_URL",
        "http://127.0.0.1:8001/api/proyectar"
    )

    # ------------------------------------------------------------
    # PAYLOAD A ENVIAR AL MICROSERVICIO
    #
    # FastAPI recibirá estos valores como un cuerpo JSON.
    # ------------------------------------------------------------
    payload = {
        "especie": especie_nombre,
        "historico": historico,
        "meses_a_proyectar": meses_a_proyectar,
    }

    # ------------------------------------------------------------
    # LLAMADA HTTP AL MICROSERVICIO
    #
    # requests.post():
    #   - json=payload      → envía JSON automáticamente
    #   - timeout=5         → evita que la vista se quede colgada
    #
    # raise_for_status():
    #   - lanza excepción para cualquier código >= 400
    #     permitiendo manejar errores arriba.
    # ------------------------------------------------------------
    resp = requests.post(url, json=payload, timeout=5)
    resp.raise_for_status()

    # ------------------------------------------------------------
    # Retorna el JSON ya decodificado en un dict de Python
    # ------------------------------------------------------------
    return resp.json()

