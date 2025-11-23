from django.urls import path
from . import views


# ===============================================================
# URLS DEL MÓDULO AuditoriaApp
#
# Este archivo define las rutas para consultar los registros
# de auditoría del sistema. Estas vistas permiten:
#
#   ✓ Ver la lista completa de auditorías registradas
#   ✓ Ver el detalle de una auditoría individual
#
# Seguridad:
#   Todas las vistas están protegidas por el decorador:
#       @requiere_permiso("PermisoVerDashboard")
#   Esto garantiza que solo usuarios con rol autorizado
#   (por ejemplo: Admin o Gerente) puedan acceder.
#
# Convención de nombres:
#   name="auditoria"           → listado general
#   name="auditoria_detalle"   → detalle de un registro específico
#
# Integración:
#   Estas rutas se incluyen normalmente bajo:
#       /auditoria/
#   dentro del router principal (HomeApp/urls.py).
# ===============================================================

urlpatterns = [

    # -----------------------------------------------------------
    # LISTA DE AUDITORÍAS
    #
    # URL: /
    # Vista: auditoria_list
    # Descripción:
    #   Muestra todas las auditorías ordenadas por fecha
    #   descendente (eventos más recientes primero).
    # -----------------------------------------------------------
    path("", views.auditoria_list, name="auditoria"),

    # -----------------------------------------------------------
    # DETALLE DE UNA AUDITORÍA ESPECÍFICA
    #
    # URL: /detalle/<id>/
    # Vista: auditoria_detalle
    # Descripción:
    #   Muestra la información completa de una auditoría:
    #       - usuario
    #       - acción realizada
    #       - módulo afectado
    #       - detalle
    #       - fecha/hora
    # -----------------------------------------------------------
    path("detalle/<int:id>/", views.auditoria_detalle, name="auditoria_detalle"),
]
