# ProyeccionesApp/views.py
from django.shortcuts import redirect
from django.contrib import messages

from .services import generar_proyecciones_automaticas

def actualizar_proyecciones(request):
    """
    Llama al microservicio, genera proyecciones y las guarda en MongoDB.
    Luego redirige al dashboard principal.
    """
    generar_proyecciones_automaticas()
    messages.success(request, "Proyecciones actualizadas desde el microservicio.")
    return redirect("dashboard")