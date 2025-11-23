from django.shortcuts import render
from RolApp.decorators import requiere_permiso

# Utilidades Django
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

# Modelo de auditoría
from .models import Auditoria


# ===============================================================
# MÓDULO AuditoriaApp — VISTAS
#
# Este módulo permite visualizar:
#   - Listado completo de auditorías del sistema
#   - Detalle de auditoría individual
#
# Importancia:
#   El modelo Auditoria registra acciones críticas en el sistema:
#       • Creación / edición / eliminación de entidades
#       • Inicio / cierre de sesión
#       • Operaciones administrativas
#
# Seguridad:
#   Ambas vistas están protegidas por:
#       @requiere_permiso("PermisoVerDashboard")
#   Esto significa que únicamente roles autorizados
#   (Administrador, Gerente) pueden ver los registros.
# ===============================================================


# ===============================================================
# LISTADO DE AUDITORÍAS
#
# Decorador:
#   @requiere_permiso("PermisoVerDashboard")
#
# Función:
#   - Obtiene todas las auditorías registradas
#   - Orden descendente por fecha (últimas primero)
#   - Renderiza la plantilla auditoria/lista.html
#
# Contexto enviado al template:
#   auditorias → queryset con todas las auditorías
# ===============================================================
@requiere_permiso("PermisoVerDashboard")
def auditoria_list(request):
    auditorias = Auditoria.objects.all().order_by("-fecha")
    return render(request, "auditoria/lista.html", {"auditorias": auditorias})


# ===============================================================
# DETALLE DE UNA AUDITORÍA
#
# Decorador:
#   @requiere_permiso("PermisoVerDashboard")
#
# Función:
#   - Obtiene una auditoría por ID
#   - Si no existe, genera un 404
#   - Renderiza auditoria/detalle.html
#
# Contexto enviado al template:
#   a → objeto Auditoria
# ===============================================================
@requiere_permiso("PermisoVerDashboard")
def auditoria_detalle(request, id):
    a = get_object_or_404(Auditoria, id=id)
    return render(request, "auditoria/detalle.html", {"a": a})
