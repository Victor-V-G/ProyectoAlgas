# Create your models here.
from django.db import models
from UsuariosApp.models import UsuariosModels


# ===============================================================
# MODELO: Auditoria
#
# Este modelo registra todas las acciones importantes realizadas
# dentro del sistema. Es clave para:
#
#   ✓ Trazabilidad de cambios
#   ✓ Monitoreo de actividades por usuario
#   ✓ Seguridad y control de acciones críticas
#   ✓ Auditorías internas del sistema
#
# Este registro se crea automáticamente mediante:
#   • Decorador @auditar
#   • Función registrar_auditoria()
#
# Cada registro incluye:
#   - Usuario involucrado (si existe)
#   - Tipo de acción (crear, editar, eliminar, login, logout, etc.)
#   - Módulo afectado (Stock, Contratos, Especies, Insumos…)
#   - Detalle descriptivo adicional
#   - Fecha/hora exacta del evento
#
# ===============================================================
class Auditoria(models.Model):

    # -----------------------------------------------------------
    # Usuario que realizó la acción
    #
    # on_delete=models.SET_NULL :
    #   Si el usuario fuera eliminado del sistema, la auditoría
    #   NO se elimina. En su lugar, el campo usuario se vuelve NULL.
    #
    # Esto preserva la trazabilidad histórica a largo plazo.
    # -----------------------------------------------------------
    usuario = models.ForeignKey(
        UsuariosModels,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Usuario responsable de la acción (puede ser NULL)."
    )

    # -----------------------------------------------------------
    # Acción realizada
    #
    # Ejemplos:
    #   crear
    #   editar
    #   eliminar
    #   login
    #   logout
    #   asignar_rol
    #
    # Este campo permite identificar rápidamente el tipo de evento.
    # -----------------------------------------------------------
    accion = models.CharField(
        max_length=50,
        help_text="Tipo de acción ejecutada (crear, editar, eliminar...)."
    )

    # -----------------------------------------------------------
    # Módulo o sección del sistema donde ocurrió la acción
    #
    # Ejemplos:
    #   "Contrato"
    #   "Stock"
    #   "Insumos"
    #   "Especie"
    #   "Autenticación"
    # -----------------------------------------------------------
    modulo = models.CharField(
        max_length=100,
        help_text="Módulo o entidad afectada por la acción."
    )

    # -----------------------------------------------------------
    # Detalle adicional
    #
    # Información extendida sobre la acción. Ejemplos:
    #   "Creado contrato para cliente X"
    #   "Maxisaco editado (ID 21)"
    #   "Inicio de sesión fallido"
    #
    # Es opcional para permitir auditorías simples.
    # -----------------------------------------------------------
    detalle = models.TextField(
        blank=True,
        null=True,
        help_text="Detalle descriptivo opcional de la acción realizada."
    )

    # -----------------------------------------------------------
    # Fecha y hora del evento
    #
    # auto_now_add=True :
    #   Registra automáticamente el momento exacto de creación,
    #   sin posibilidad de ser modificado manualmente.
    #
    # Esto garantiza precisión en la trazabilidad.
    # -----------------------------------------------------------
    fecha = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora en que ocurrió la acción."
    )

    # -----------------------------------------------------------
    # Representación legible del registro de auditoría
    # -----------------------------------------------------------
    def __str__(self):
        return f"{self.modulo} - {self.accion} ({self.fecha:%d/%m/%Y %H:%M})"
