from django.urls import path
from . import views


# ===============================================================
# URLS DEL MÓDULO EspecieApp
#
# Este archivo define todas las rutas relacionadas con la
# administración de especies de algas dentro del sistema.
#
# Todas las vistas están protegidas por permisos usando el
# decorador @requiere_permiso("PermisoEditarStock"), por lo que
# solo usuarios autorizados pueden acceder.
#
# Rutas incluidas:
#   - Listar especies
#   - Crear especie
#   - Editar especie
#   - Eliminar especie
#   - Detalle de especie
#
# Convención:
#   name="especies"          → listado principal
#   name="especie_crear"    → formulario de creación
#   name="especie_editar"   → formulario de edición
#   name="especie_eliminar" → acción eliminar
#   name="especie_detalle"  → ver detalles
# ===============================================================

urlpatterns = [

    # -----------------------------------------------------------
    # LISTAR ESPECIES
    # GET /
    # Vista: especies_list
    # -----------------------------------------------------------
    path("", views.especies_list, name="especies"),

    # -----------------------------------------------------------
    # CREAR NUEVA ESPECIE
    # GET  /crear/     → formulario
    # POST /crear/     → registrar especie
    # Vista: especie_crear
    # -----------------------------------------------------------
    path("crear/", views.especie_crear, name="especie_crear"),

    # -----------------------------------------------------------
    # EDITAR ESPECIE EXISTENTE
    # GET  /editar/<id>/ → formulario con datos
    # POST /editar/<id>/ → guardar cambios
    # Vista: especie_editar
    # -----------------------------------------------------------
    path("editar/<int:id>/", views.especie_editar, name="especie_editar"),

    # -----------------------------------------------------------
    # ELIMINAR ESPECIE
    # GET  /eliminar/<id>/
    # Acción directa que elimina la especie
    # Vista: especie_eliminar
    # -----------------------------------------------------------
    path("eliminar/<int:id>/", views.especie_eliminar, name="especie_eliminar"),

    # -----------------------------------------------------------
    # DETALLE DE UNA ESPECIE
    # GET /<id>/
    # Vista: especie_detalle
    # -----------------------------------------------------------
    path("<int:id>/", views.especie_detalle, name="especie_detalle"),
]
