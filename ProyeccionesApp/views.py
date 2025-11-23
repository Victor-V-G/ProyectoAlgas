# ===============================================================
# ProyeccionesApp/views.py
#
# Vista responsable de actualizar las proyecciones ejecutivas del
# sistema mediante un microservicio interno definido en:
#       ProyeccionesApp/services.py
#
# Esta vista:
#   - Requiere permisos específicos (PermisoCrearContratos)
#   - Invoca un servicio que genera/actualiza datos
#   - Redirige al dashboard con un mensaje de éxito
# ===============================================================

from django.shortcuts import redirect
from django.contrib import messages
from RolApp.decorators import requiere_permiso
from .services import generar_proyecciones_automaticas


# ===============================================================
# VISTA: actualizar_proyecciones
#
# Decorador:
#   @requiere_permiso("PermisoCrearContratos")
#     → Solo usuarios con este permiso pueden actualizar
#       las proyecciones ejecutivas.
#
# Lógica:
#   1. Llama al microservicio generar_proyecciones_automaticas()
#   2. Muestra un mensaje de confirmación
#   3. Redirige al dashboard
#
# Esta vista no devuelve HTML; solo ejecuta lógica interna.
# ===============================================================
@requiere_permiso("PermisoCrearContratos")
def actualizar_proyecciones(request):

    # -----------------------------------------------------------
    # LLAMADA AL MICROSERVICIO (services.py)
    #
    # Este servicio se encarga de:
    #   - recalcular proyecciones mensuales
    #   - actualizar cifras estimadas
    #   - consumir datos de modelos / APIs / Mongo / etc.
    # -----------------------------------------------------------
    generar_proyecciones_automaticas()

    # -----------------------------------------------------------
    # MENSAJE DE ÉXITO
    # Se muestra en el dashboard gracias al sistema de messages.
    # -----------------------------------------------------------
    messages.success(request, "Proyecciones actualizadas desde el microservicio.")

    # -----------------------------------------------------------
    # REDIRECCIÓN
    # Retorna al dashboard ejecutivo una vez finalizado el proceso.
    # -----------------------------------------------------------
    return redirect("dashboard")
