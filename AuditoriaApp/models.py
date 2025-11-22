
# Create your models here.
from django.db import models
from UsuariosApp.models import UsuariosModels

class Auditoria(models.Model):
    usuario = models.ForeignKey(
        UsuariosModels,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    accion = models.CharField(max_length=50)  # crear / actualizar / eliminar
    modulo = models.CharField(max_length=100)  # Ej: "Contrato", "Stock", "Especie"
    detalle = models.TextField(blank=True, null=True)

    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.modulo} - {self.accion} ({self.fecha:%d/%m/%Y %H:%M})"
