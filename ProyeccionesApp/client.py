# ProyeccionesApp/client.py
import requests
from django.conf import settings


def llamar_microservicio_proyecciones(especie_nombre: str, historico: list, meses_a_proyectar: int = 12) -> dict:
    """
    Llama al microservicio FastAPI para generar proyecciones.

    historico: lista de dicts con:
        { "anio": int, "mes": int, "toneladas": float }
    """
    url = getattr(settings, "PROYECCIONES_MICRO_URL", "http://127.0.0.1:8001/api/proyectar")

    payload = {
        "especie": especie_nombre,
        "historico": historico,
        "meses_a_proyectar": meses_a_proyectar,
    }

    resp = requests.post(url, json=payload, timeout=5)
    resp.raise_for_status()
    return resp.json()
