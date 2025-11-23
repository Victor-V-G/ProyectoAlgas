from django.urls import path
from . import views


# ===============================================================
# URLS DEL MÓDULO ContratoApp
#
# Este archivo define todas las rutas para la gestión de:
#   - Contratos
#   - Entregas de contrato
#
# Todas estas vistas están protegidas mediante:
#   @requiere_permiso("PermisoCrearContratos")
#
# CONVENCIÓN DE NOMBRES:
#   name="contratos"              → listado de contratos
#   name="contrato_crear"         → crear contrato
#   name="contrato_editar"        → editar contrato
#   name="contrato_eliminar"      → eliminar contrato
#   name="contrato_detalle"       → ver entregas + información
#
#   name="entrega_crear"          → crear entrega asociada a contrato
#   name="entrega_editar"         → editar entrega existente
#
# La estructura final es un CRUD completo para contratos y entregas.
# ===============================================================

urlpatterns = [

    # -----------------------------------------------------------
    # LISTADO DE CONTRATOS
    # GET /
    # Vista: contratos_list
    # -----------------------------------------------------------
    path("", views.contratos_list, name="contratos"),

    # -----------------------------------------------------------
    # CREAR CONTRATO
    # GET  /crear/     → formulario vacío
    # POST /crear/     → guardar contrato
    # Vista: contrato_crear
    # -----------------------------------------------------------
    path("crear/", views.contrato_crear, name="contrato_crear"),

    # -----------------------------------------------------------
    # EDITAR CONTRATO
    # GET  /editar/<id>/ → formulario precargado
    # POST /editar/<id>/ → actualizar contrato
    # Vista: contrato_editar
    # -----------------------------------------------------------
    path("editar/<int:id>/", views.contrato_editar, name="contrato_editar"),

    # -----------------------------------------------------------
    # ELIMINAR CONTRATO
    # GET /eliminar/<id>/
    # Vista: contrato_eliminar
    # -----------------------------------------------------------
    path("eliminar/<int:id>/", views.contrato_eliminar, name="contrato_eliminar"),

    # -----------------------------------------------------------
    # DETALLE DE CONTRATO (+ entregas asociadas)
    # GET /<id>/
    # Vista: contrato_detalle
    # -----------------------------------------------------------
    path("<int:id>/", views.contrato_detalle, name="contrato_detalle"),


    # ===========================================================
    # ENTREGAS DE CONTRATO
    # ===========================================================

    # -----------------------------------------------------------
    # CREAR ENTREGA PARA UN CONTRATO ESPECÍFICO
    #
    # Ruta:
    #   /<contrato_id>/entrega/crear/
    #
    # Vista:
    #   entrega_crear
    #
    # Nota:
    #   Se accede desde el detalle del contrato.
    # -----------------------------------------------------------
    path("<int:contrato_id>/entrega/crear/", views.entrega_crear, name="entrega_crear"),

    # -----------------------------------------------------------
    # EDITAR ENTREGA YA REGISTRADA
    #
    # Ruta:
    #   /entrega/editar/<id>/
    #
    # Vista:
    #   entrega_editar
    #
    # Nota:
    #   Al finalizar, redirige al detalle del contrato.
    # -----------------------------------------------------------
    path("entrega/editar/<int:id>/", views.entrega_editar, name="entrega_editar"),
]
