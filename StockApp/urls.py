from django.urls import path
from . import views

# ============================================================
# URLs de la aplicación de Stock (StockApp)
#
# Cada ruta:
#   - Apunta a una vista específica definida en views.py
#   - Lleva un "name" para poder invocarla desde plantillas
#   - Algunas reciben parámetros como <int:id>
#
# Estructura general:
#   /stock/             → lista
#   /stock/crear/       → crear nuevo registro
#   /stock/editar/ID/   → editar registro existente
#   /stock/eliminar/ID/ → eliminar registro existente
#   /stock/ID/          → detalle del registro
# ============================================================
urlpatterns = [

    # ------------------------------------------------------------
    # LISTAR STOCK
    # Ruta raíz de la aplicación:
    #   /stock/
    #
    # Muestra todos los registros de Maxisacos.
    # ------------------------------------------------------------
    path("", views.stock_list, name="stock"),

    # ------------------------------------------------------------
    # CREAR REGISTRO DE STOCK
    # Ruta:
    #   /stock/crear/
    #
    # Permite crear un nuevo Maxisaco mediante un formulario.
    # ------------------------------------------------------------
    path("crear/", views.stock_crear, name="stock_crear"),

    # ------------------------------------------------------------
    # EDITAR REGISTRO EXISTENTE
    # Ruta:
    #   /stock/editar/ID/
    #
    # <int:id> indica el ID del registro a modificar.
    # ------------------------------------------------------------
    path("editar/<int:id>/", views.stock_editar, name="stock_editar"),

    # ------------------------------------------------------------
    # ELIMINAR REGISTRO
    # Ruta:
    #   /stock/eliminar/ID/
    #
    # Elimina un Maxisaco específico.
    # ------------------------------------------------------------
    path("eliminar/<int:id>/", views.stock_eliminar, name="stock_eliminar"),

    # ------------------------------------------------------------
    # DETALLE DEL REGISTRO
    # Ruta:
    #   /stock/ID/
    #
    # Muestra los datos completos del registro seleccionado.
    # ------------------------------------------------------------
    path("<int:id>/", views.stock_detalle, name="stock_detalle"),
]
