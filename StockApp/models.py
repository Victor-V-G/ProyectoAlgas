from django.db import models
from django.conf import settings
from EspecieApp.models import Especie
from UsuariosApp.models import UsuariosModels  # tu modelo REAL de usuario


class Maxisaco(models.Model):
    especie = models.ForeignKey(Especie, on_delete=models.PROTECT)
    peso_kg = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    # Usuario que registró el maxisaco
    registrado_por = models.ForeignKey(
        UsuariosModels,   # ← CORREGIDO, YA NO USA AUTH_USER_MODEL
        on_delete=models.PROTECT,
        related_name="maxisacos_registrados"
    )

    # Entrada o salida
    tipo_movimiento = models.CharField(
        max_length=10,
        choices=[
            ("entrada", "Entrada"),
            ("salida", "Salida"),
        ]
    )

    # Auditoría
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    actualizado_por = models.ForeignKey(
        UsuariosModels,   # ← CORREGIDO
        on_delete=models.PROTECT,
        related_name="maxisacos_actualizados",
        null=True,
        blank=True
    )

    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.especie.nombre} - {self.peso_kg} kg ({self.tipo_movimiento})"
