from django.db import models
from UsuariosApp.models import UsuariosModels


# ===============================================================
# MODELO: Contrato
#
# Representa un contrato comercial con un cliente, indicando:
#   - Cliente asociado
#   - Tonelaje total comprometido
#   - Rango de fechas del contrato
#   - Estado del contrato (activo, completado, cancelado)
#
# Auditado mediante:
#   - creado_por / actualizado_por (usuario del sistema)
#   - fechas automáticas de creación/actualización
#
# Relación:
#   Un contrato puede tener muchas entregas → EntregaContrato
#   (related_name="entregas")
# ===============================================================
class Contrato(models.Model):

    # -----------------------------------------------------------
    # Nombre del cliente asociado al contrato
    # -----------------------------------------------------------
    cliente = models.CharField(
        max_length=200,
        help_text="Nombre del cliente asociado al contrato."
    )

    # -----------------------------------------------------------
    # Tonelaje total acordado en el contrato (en toneladas)
    # -----------------------------------------------------------
    tonelaje_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Tonelaje total comprometido en el contrato."
    )

    # -----------------------------------------------------------
    # Fecha en que inicia y finaliza el contrato
    # -----------------------------------------------------------
    fecha_inicio = models.DateField(
        help_text="Fecha de inicio del contrato."
    )
    fecha_fin = models.DateField(
        help_text="Fecha de término del contrato."
    )

    # -----------------------------------------------------------
    # Auditoría: usuario creador del contrato
    #
    # on_delete=models.PROTECT:
    #   Impide eliminar al usuario si tiene contratos asociados
    # -----------------------------------------------------------
    creado_por = models.ForeignKey(
        UsuariosModels,
        on_delete=models.PROTECT,
        related_name="contratos_creados",
        help_text="Usuario que registró el contrato."
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha en que el contrato fue creado."
    )

    # -----------------------------------------------------------
    # Auditoría: último usuario que modificó el contrato
    # -----------------------------------------------------------
    actualizado_por = models.ForeignKey(
        UsuariosModels,
        on_delete=models.PROTECT,
        related_name="contratos_actualizados",
        help_text="Usuario que realizó la última actualización."
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        help_text="Última fecha de modificación del contrato."
    )

    # -----------------------------------------------------------
    # Estado del contrato
    #
    #   activo      → contrato vigente
    #   completado  → contrato cumplido
    #   cancelado   → contrato terminado antes de tiempo
    # -----------------------------------------------------------
    estado = models.CharField(
        max_length=20,
        choices=[
            ("activo", "Activo"),
            ("completado", "Completado"),
            ("cancelado", "Cancelado"),
        ],
        default="activo",
        help_text="Estado actual del contrato."
    )

    # -----------------------------------------------------------
    # Representación legible
    # -----------------------------------------------------------
    def __str__(self):
        return f"Contrato #{self.id} - {self.cliente}"


# ===============================================================
# MODELO: EntregaContrato
#
# Representa una entrega mensual programada dentro de un contrato.
#
# Cada entrega incluye:
#   - Mes de entrega
#   - Toneladas requeridas (plan)
#   - Toneladas cumplidas (avance real)
#
# Relación:
#   Una entrega pertenece a un contrato → ForeignKey
#   Cuando se elimina el contrato, se eliminan sus entregas
#   (on_delete=models.CASCADE)
#
# Este modelo es clave para:
#   - Calcular cumplimiento contractual
#   - Dashboard ejecutivo
#   - Proyecciones comparativas
# ===============================================================
from EspecieApp.models import Especie

class EntregaContrato(models.Model):

    contrato = models.ForeignKey(
        Contrato,
        on_delete=models.CASCADE,
        related_name="entregas",
        help_text="Contrato al cual pertenece esta entrega."
    )

    mes = models.DateField(
        help_text="Mes correspondiente a la entrega (usar día 1)."
    )

    toneladas_requeridas = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Kilogramos que deben ser entregados en el mes."
    )

    toneladas_cumplidas = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Kilogramos efectivamente entregados."
    )

    especie = models.ForeignKey(
        Especie,
        on_delete=models.PROTECT,
        related_name="entregas",
        help_text="Especie de alga correspondiente a esta entrega."
    )

    
    compromiso_sin_stock = models.BooleanField(
        default=False,
        help_text="Indica si la entrega fue comprometida sin stock disponible."
    )

    fecha_limite = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha límite de cumplimiento cuando se compromete sin stock."
    )

    def __str__(self):
        return f"Entrega {self.mes} - {self.toneladas_requeridas} KG"
