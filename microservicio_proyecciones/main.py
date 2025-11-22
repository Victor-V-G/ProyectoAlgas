# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class HistoricoMes(BaseModel):
    anio: int
    mes: int
    toneladas: float


class RequestProyecciones(BaseModel):
    especie: str
    historico: List[HistoricoMes]
    meses_a_proyectar: int = 12


class MesProyectado(BaseModel):
    anio: int
    mes: int
    proyeccion_ton: float


class ResponseProyecciones(BaseModel):
    especie: str
    proyecciones: List[MesProyectado]


@app.post("/api/proyectar", response_model=ResponseProyecciones)
def proyectar(req: RequestProyecciones):
    """
    Modelo simple:
    - Saca el promedio de las toneladas históricas.
    - Aplica un +5% de tendencia de crecimiento.
    - Genera N meses hacia adelante (meses_a_proyectar).
    """

    if not req.historico:
        return ResponseProyecciones(especie=req.especie, proyecciones=[])

    # Promedio simple
    promedio = sum(h.toneladas for h in req.historico) / len(req.historico)
    base = promedio * 1.05  # +5% tendencia

    # Determinar desde qué año/mes proyectar
    ultimo = max(req.historico, key=lambda x: (x.anio, x.mes))
    anio = ultimo.anio
    mes = ultimo.mes

    proyecciones: List[MesProyectado] = []

    for _ in range(req.meses_a_proyectar):
        # Avanzar mes
        mes += 1
        if mes > 12:
            mes = 1
            anio += 1

        proyecciones.append(
            MesProyectado(
                anio=anio,
                mes=mes,
                proyeccion_ton=round(base, 2),
            )
        )

    return ResponseProyecciones(
        especie=req.especie,
        proyecciones=proyecciones
    )
