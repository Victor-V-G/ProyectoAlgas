# ProyeccionesApp/views.py

from django.shortcuts import redirect
from django.contrib import messages
from RolApp.decorators import requiere_permiso
from .services import generar_proyecciones_automaticas


@requiere_permiso("PermisoCrearContratos")
def actualizar_proyecciones(request):
    generar_proyecciones_automaticas()
    messages.success(request, "Proyecciones actualizadas desde el microservicio.")
    return redirect("dashboard")
