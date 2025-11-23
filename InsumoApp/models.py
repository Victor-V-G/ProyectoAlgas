from django.db import models
from UsuariosApp.models import UsuariosModels


# ===============================================================
# MODELO: Insumo
#
# Representa un insumo utilizado dentro del sistema de gestión.
# Cada insumo puede ser:
#   - materia prima
#   - producto consumible
#   - material operativo
#
# Este modelo soporta:
#   - control de stock
#   - umbrales mínimos de seguridad
#   - auditoría completa (creado y actualizado por)
# ===============================================================
class Insumo(models.Model):

    # -----------------------------------------------------------
    # Nombre del insumo
    #
    # - Debe ser único
    # - Máx. 200 caracteres
    #
    # Ejemplos:
    #   "Sacos plásticos"
    #   "Sal industrial"
    #   "Aditivo químico"
    # -----------------------------------------------------------
    nombre = models.CharField(
        max_length=200,
        unique=True
    )

    # -----------------------------------------------------------
    # Descripción detallada del insumo
    #
    # - Opcional
    # - Permite notas operativas, especificaciones, etc.
    # -----------------------------------------------------------
    descripcion = models.TextField(
        blank=True,
        null=True
    )

    # -----------------------------------------------------------
    # Cantidad actual disponible
    #
    # - Decimal para permitir valores precisos
    # - Puede representar kg, litros o unidades
    # -----------------------------------------------------------
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # -----------------------------------------------------------
    # Unidad de medida del insumo
    #
    # "kg" → kilogramo  
    # "lt" → litro  
    # "un" → unidades  
    #
    # Estos valores determinan cómo interpretar la cantidad.
    # -----------------------------------------------------------
    unidad = models.CharField(
        max_length=20,
        choices=[
            ("kg", "Kilogramos"),
            ("lt", "Litros"),
            ("un", "Unidades"),
        ]
    )

    # -----------------------------------------------------------
    # Mínimo de seguridad
    #
    # Cuando la cantidad sea menor o igual a este valor,
    # el sistema debe disparar alertas.
    # -----------------------------------------------------------
    minimo_seguridad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Cantidad mínima para activar alerta"
    )

    # ===========================================================
    # AUDITORÍA
    # ===========================================================

    # -----------------------------------------------------------
    # Usuario que creó el insumo
    #
    # - PROTECT evita borrar usuarios que tengan insumos
    # -----------------------------------------------------------
    creado_por = models.ForeignKey(
        UsuariosModels,
        on_delete=models.PROTECT,
        related_name="insumos_creados"
    )

    # Fecha de creación del registro
    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    # -----------------------------------------------------------
    # Usuario que realizó la última actualización
    # - Es opcional para permitir que existan registros sin actualizar
    # -----------------------------------------------------------
    actualizado_por = models.ForeignKey(
        UsuariosModels,
        on_delete=models.PROTECT,
        related_name="insumos_actualizados",
        null=True,
        blank=True
    )

    # Fecha de la última actualización
    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    # ===========================================================
    # MÉTODOS PERSONALIZADOS
    # ===========================================================

    # -----------------------------------------------------------
    # estado_stock()
    #
    # Devuelve:
    #   - "sin_stock" → cantidad = 0 o menor
    #   - "bajo" → cantidad ≤ mínimo de seguridad
    #   - "normal" → cantidad suficiente
    #
    # Esto es útil para:
    #   - Mostrar colores en tabla
    #   - Alertas visuales
    #   - Lógica de dashboard
    # -----------------------------------------------------------
    def estado_stock(self):
        if self.cantidad <= 0:
            return "sin_stock"
        elif self.cantidad <= self.minimo_seguridad:
            return "bajo"
        return "normal"

    # -----------------------------------------------------------
    # Representación legible del objeto
    # -----------------------------------------------------------
    def __str__(self):
        return self.nombre
