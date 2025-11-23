from django.db import models
from EspecieApp.models import Especie
from UsuariosApp.models import UsuariosModels  # Modelo real de usuario del sistema


# ================================================================
# MODELO: Maxisaco
#
# Representa un registro de stock de un "maxisaco" de alga,
# indicando:
#   - especie almacenada
#   - peso total
#   - tipo (entrada/salida)
#   - usuario que creó el registro
#   - usuario que lo actualizó
#   - timestamps automáticos
#
# Este modelo forma parte del módulo de Stock.
# ================================================================
class Maxisaco(models.Model):

    # ------------------------------------------------------------
    # ESPECIE
    # Relación con el modelo Especie.
    # Cada Maxisaco pertenece a una sola especie.
    #
    # on_delete=PROTECT:
    #   → Evita borrar una especie si está siendo usada.
    # ------------------------------------------------------------
    especie = models.ForeignKey(Especie, on_delete=models.PROTECT)

    # ------------------------------------------------------------
    # PESO EN KILOGRAMOS
    # Almacena peso con precisión decimal (hasta 2 decimales).
    #
    # max_digits=10 → hasta 9 dígitos + 1 decimal
    # decimal_places=2 → precisión de dos decimales
    # Ejemplo válido: 12345.67
    # ------------------------------------------------------------
    peso_kg = models.DecimalField(max_digits=10, decimal_places=2)

    # ------------------------------------------------------------
    # FECHA DE REGISTRO
    # Se asigna automáticamente al crear el Maxisaco.
    #
    # auto_now_add=True:
    #   → fecha exacta en que se creó el registro.
    # ------------------------------------------------------------
    fecha_registro = models.DateTimeField(auto_now_add=True)

    # ------------------------------------------------------------
    # USUARIO QUE REGISTRÓ EL MAXISACO
    #
    # PROTECT:
    #   → evita eliminar usuarios involucrados en registros.
    #
    # related_name="maxisacos_registrados":
    #   → permite acceder desde usuario.maxisacos_registrados.all()
    # ------------------------------------------------------------
    registrado_por = models.ForeignKey(
        UsuariosModels,
        on_delete=models.PROTECT,
        related_name="maxisacos_registrados"
    )

    # ------------------------------------------------------------
    # TIPO DE MOVIMIENTO
    #
    # Indica si el registro corresponde a:
    #   - "entrada": ingreso a bodega
    #   - "salida": extracción o venta
    #
    # choices:
    #   → limita los valores permitidos en la BD.
    # ------------------------------------------------------------
    tipo_movimiento = models.CharField(
        max_length=10,
        choices=[
            ("entrada", "Entrada"),
            ("salida", "Salida"),
        ]
    )

    # ------------------------------------------------------------
    # FECHA DE ÚLTIMA ACTUALIZACIÓN
    #
    # auto_now=True:
    #   → se actualiza automáticamente cada vez que se guarda el objeto.
    # ------------------------------------------------------------
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    # ------------------------------------------------------------
    # USUARIO QUE REALIZÓ LA ÚLTIMA ACTUALIZACIÓN
    #
    # null=True y blank=True:
    #   → permite que inicialmente esté vacío
    #
    # related_name:
    #   → acceso desde usuario.maxisacos_actualizados.all()
    #
    # PROTECT:
    #   → NO permite eliminar usuarios con actividad registrada.
    # ------------------------------------------------------------
    actualizado_por = models.ForeignKey(
        UsuariosModels,
        on_delete=models.PROTECT,
        related_name="maxisacos_actualizados",
        null=True,
        blank=True
    )

    # ------------------------------------------------------------
    # OBSERVACIONES
    # Campo opcional para notas adicionales.
    #
    # blank=True → permitido vacío en formularios
    # null=True  → permitido vacío en base de datos
    # ------------------------------------------------------------
    observaciones = models.TextField(blank=True, null=True)

    # ------------------------------------------------------------
    # REPRESENTACIÓN EN TEXTO
    #
    # Muestra especie, peso y tipo de movimiento.
    # Útil en Django Admin, logs y auditorías.
    # ------------------------------------------------------------
    def __str__(self):
        return f"{self.especie.nombre} - {self.peso_kg} kg ({self.tipo_movimiento})"
