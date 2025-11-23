# ===============================================================
# MODELO: Especie
#
# Representa un tipo de alga registrada en el sistema.
# Es utilizado en:
#   - Módulo de Stock (Maxisaco)
#   - Contratos
#   - Proyecciones (microservicio)
#   - Dashboard ejecutivo
#
# Incluye:
#   - Nombre (único)
#   - Descripción
#   - Proporción de conversión húmedo→seco
#   - Fechas de auditoría automática
#
# Este modelo es *base* dentro del dominio de datos del sistema.
# ===============================================================

from django.db import models


class Especie(models.Model):

    # -----------------------------------------------------------
    # Nombre único de la especie
    #
    # Ejemplos:
    #   - Luga Roja
    #   - Pelillo
    #   - Huiro
    #
    # Se usa como referencia en:
    #   - Stock (Maxisaco)
    #   - Proyecciones
    #   - Vistas de inventario
    # -----------------------------------------------------------
    nombre = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nombre único de la especie de alga."
    )

    # -----------------------------------------------------------
    # Descripción general de la especie
    # Opcional: permite dar contexto, características o notas internas
    # -----------------------------------------------------------
    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text="Descripción opcional de la especie."
    )

    # -----------------------------------------------------------
    # Proporción de conversión húmedo → seco
    #
    # Ejemplo:
    #   6.00 significa:
    #       6 kg húmedos ≈ 1 kg seco
    #
    # Este valor es **clave** en procesos de:
    #   - Cálculos productivos
    #   - Evaluaciones de rendimiento
    #   - Modelos predictivos (microservicio de proyecciones)
    # -----------------------------------------------------------
    proporcion_conversion = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Ejemplo: 6.00 para una proporción 6:1 (húmedo a seco)."
    )

    # -----------------------------------------------------------
    # Fechas de auditoría automática
    #
    # fecha_creacion:
    #     - Se asigna solo una vez
    #
    # fecha_actualizacion:
    #     - Se actualiza cada vez que el registro es modificado
    # -----------------------------------------------------------
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha en que la especie fue registrada."
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        help_text="Última modificación del registro."
    )

    # -----------------------------------------------------------
    # Representación textual del objeto
    # Usado en admin, logs, selects, etc.
    # -----------------------------------------------------------
    def __str__(self):
        return self.nombre

