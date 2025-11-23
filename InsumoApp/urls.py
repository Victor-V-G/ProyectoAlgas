from django.urls import path
from . import views

# ===============================================================
# InsumoApp/urls.py
#
# Define todas las rutas del módulo de Insumos.
#
# Funcionalidades cubiertas:
#   - Listar insumos
#   - Crear insumo
#   - Editar insumo
#   - Ver detalle de un insumo
#   - Eliminar insumo
#
# Todas estas vistas requieren permisos del rol:
#   PermisoEditarStock
#
# Además, las acciones CRUD registran auditoría mediante:
#   @auditar(...)
# ===============================================================
urlpatterns = [

    # -----------------------------------------------------------
    # LISTADO GENERAL DE INSUMOS
    #
    # URL:
    #     /insumos/
    #
    # Vista:
    #     insumos_list
    #
    # Nombre:
    #     "insumos"
    #
    # Muestra el listado completo de insumos en el sistema.
    # -----------------------------------------------------------
    path("", views.insumos_list, name="insumos"),

    # -----------------------------------------------------------
    # CREAR NUEVO INSUMO
    #
    # URL:
    #     /insumos/crear/
    #
    # Vista:
    #     insumo_crear
    #
    # Nombre:
    #     "insumo_crear"
    #
    # Muestra formulario + procesa creación.
    # Registra auditoría.
    # -----------------------------------------------------------
    path("crear/", views.insumo_crear, name="insumo_crear"),

    # -----------------------------------------------------------
    # EDITAR INSUMO EXISTENTE
    #
    # URL:
    #     /insumos/editar/<id>/
    #
    # Vista:
    #     insumo_editar
    #
    # Nombre:
    #     "insumo_editar"
    #
    # Muestra formulario de edición + actualiza datos.
    # Registra auditoría.
    # -----------------------------------------------------------
    path("editar/<int:id>/", views.insumo_editar, name="insumo_editar"),

    # -----------------------------------------------------------
    # DETALLE DE INSUMO
    #
    # URL:
    #     /insumos/detalle/<id>/
    #
    # Vista:
    #     insumo_detalle
    #
    # Nombre:
    #     "insumo_detalle"
    #
    # Muestra toda la información de un insumo.
    # -----------------------------------------------------------
    path("detalle/<int:id>/", views.insumo_detalle, name="insumo_detalle"),

    # -----------------------------------------------------------
    # ELIMINAR INSUMO
    #
    # URL:
    #     /insumos/eliminar/<id>/
    #
    # Vista:
    #     insumo_eliminar
    #
    # Nombre:
    #     "insumo_eliminar"
    #
    # Elimina el registro y registra auditoría.
    # -----------------------------------------------------------
    path("eliminar/<int:id>/", views.insumo_eliminar, name="insumo_eliminar"),
]
