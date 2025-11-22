
# Create your models here.
from django.db import models

class Especie(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    # Proporción de conversión húmedo → seco (Ej: 6:1 → 6.0)
    proporcion_conversion = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Ejemplo: 6.00 para una proporción 6:1"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
