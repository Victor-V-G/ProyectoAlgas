from django.db import models
from UsuariosApp.models import UsuariosModels


class Insumo(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(
        max_length=20,
        choices=[
            ("kg", "Kilogramos"),
            ("lt", "Litros"),
            ("un", "Unidades"),
        ]
    )

    minimo_seguridad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Cantidad mínima para activar alerta"
    )

    # Auditoría
    creado_por = models.ForeignKey(
        UsuariosModels,
        on_delete=models.PROTECT,
        related_name="insumos_creados"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    actualizado_por = models.ForeignKey(
        UsuariosModels,
        on_delete=models.PROTECT,
        related_name="insumos_actualizados",
        null=True,
        blank=True
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def estado_stock(self):
        if self.cantidad <= 0:
            return "sin_stock"
        elif self.cantidad <= self.minimo_seguridad:
            return "bajo"
        return "normal"

    def __str__(self):
        return self.nombre
