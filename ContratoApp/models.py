

# Create your models here.
from django.db import models
from django.conf import settings

class Contrato(models.Model):
    cliente = models.CharField(max_length=200)
    tonelaje_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    # Auditoría
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="contratos_creados"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    actualizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="contratos_actualizados"
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    estado = models.CharField(
        max_length=20,
        choices=[
            ("activo", "Activo"),
            ("completado", "Completado"),
            ("cancelado", "Cancelado"),
        ],
        default="activo"
    )

    def __str__(self):
        return f"Contrato #{self.id} - {self.cliente}"


class EntregaContrato(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name="entregas")
    mes = models.DateField()
    toneladas_requeridas = models.DecimalField(max_digits=10, decimal_places=2)
    toneladas_cumplidas = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Entrega {self.mes} ({self.toneladas_requeridas}T)"
