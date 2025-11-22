from django.urls import path
from . import views

urlpatterns = [
    path("", views.insumos_list, name="insumos"),
    path("crear/", views.insumo_crear, name="insumo_crear"),
    path("editar/<int:id>/", views.insumo_editar, name="insumo_editar"),
    path("detalle/<int:id>/", views.insumo_detalle, name="insumo_detalle"),
    path("eliminar/<int:id>/", views.insumo_eliminar, name="insumo_eliminar"),
]
