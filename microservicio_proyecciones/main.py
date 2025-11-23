# ===============================================================
# main.py — Microservicio de Proyecciones con FastAPI
#
# Este microservicio recibe:
#   - el nombre de una especie
#   - histórico mensual de producción
#   - cantidad de meses a proyectar
#
# Y devuelve:
#   - una lista de meses futuros con una proyección estimada
#
# Algoritmo utilizado (versión simple):
#   1) Calcula promedio histórico.
#   2) Aplica +5% de tendencia de crecimiento.
#   3) Genera N meses hacia adelante.
#
# Este microservicio es consumido por Django a través de:
#   ProyeccionesApp/client.py
# ===============================================================

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


# ===============================================================
# MODELOS Pydantic (definen estructura del JSON de entrada/salida)
# ===============================================================

# ---------------------------------------------------------------
# HistoricoMes:
# Representa un registro histórico de producción mensual.
#
# Campos:
#   - anio         (int)
#   - mes          (int)
#   - toneladas    (float): toneladas ingresadas ese mes
# ---------------------------------------------------------------
class HistoricoMes(BaseModel):
    anio: int
    mes: int
    toneladas: float


# ---------------------------------------------------------------
# RequestProyecciones:
# Estructura del JSON recibido por el endpoint /api/proyectar
#
# Campos:
#   - especie              (str)
#   - historico            (list de HistoricoMes)
#   - meses_a_proyectar    (int): meses futuros a generar (default=12)
# ---------------------------------------------------------------
class RequestProyecciones(BaseModel):
    especie: str
    historico: List[HistoricoMes]
    meses_a_proyectar: int = 12


# ---------------------------------------------------------------
# MesProyectado:
# Un registro proyectado para un mes futuro.
#
# Campos:
#   - anio
#   - mes
#   - proyeccion_ton
# ---------------------------------------------------------------
class MesProyectado(BaseModel):
    anio: int
    mes: int
    proyeccion_ton: float


# ---------------------------------------------------------------
# ResponseProyecciones:
# Respuesta completa del microservicio.
#
# Campos:
#   - especie
#   - proyecciones: lista de MesProyectado
# ---------------------------------------------------------------
class ResponseProyecciones(BaseModel):
    especie: str
    proyecciones: List[MesProyectado]


# ===============================================================
# ENDPOINT PRINCIPAL DEL MICROSERVICIO
#
# POST /api/proyectar
#
# Este endpoint recibe datos históricos y genera proyecciones.
#
# Lógica del algoritmo:
#   1. Si no hay histórico → retornar lista vacía.
#   2. Promedio simple = suma(historico) / cantidad
#   3. Aplicar tendencia +5%:
#          base = promedio * 1.05
#   4. Buscar el último mes disponible del histórico.
#   5. Avanzar mes a mes generando proyecciones.
# ===============================================================
@app.post("/api/proyectar", response_model=ResponseProyecciones)
def proyectar(req: RequestProyecciones):
    """
    Algoritmo simple de ejemplo:

    - Calcula promedio de toneladas históricas.
    - Aplica un +5% de tendencia.
    - Genera 'meses_a_proyectar' meses futuros.
    """

    # Si no hay datos → no se puede proyectar
    if not req.historico:
        return ResponseProyecciones(especie=req.especie, proyecciones=[])

    # -----------------------------------------------------------
    # 1. CALCULAR PROMEDIO DEL HISTÓRICO
    # -----------------------------------------------------------
    promedio = sum(h.toneladas for h in req.historico) / len(req.historico)

    # Aplicar tendencia de crecimiento
    base = promedio * 1.05   # +5%

    # -----------------------------------------------------------
    # 2. DETERMINAR EL ÚLTIMO MES DEL HISTÓRICO
    #
    # Se toma el registro con año/mes más reciente
    # -----------------------------------------------------------
    ultimo = max(req.historico, key=lambda x: (x.anio, x.mes))
    anio = ultimo.anio
    mes = ultimo.mes

    proyecciones: List[MesProyectado] = []

    # -----------------------------------------------------------
    # 3. GENERAR MESES FUTUROS
    #
    # Se recorren N meses, avanzando año/mes correctamente:
    #   - si mes > 12 → saltar a enero y aumentar año
    # -----------------------------------------------------------
    for _ in range(req.meses_a_proyectar):
        # Avanzar mes
        mes += 1
        if mes > 12:
            mes = 1
            anio += 1

        # Crear proyección del mes
        proyecciones.append(
            MesProyectado(
                anio=anio,
                mes=mes,
                proyeccion_ton=round(base, 2),
            )
        )

    # -----------------------------------------------------------
    # 4. RETORNAR RESPUESTA
    # -----------------------------------------------------------
    return ResponseProyecciones(
        especie=req.especie,
        proyecciones=proyecciones
    )

