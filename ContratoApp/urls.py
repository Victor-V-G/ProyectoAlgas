from django.urls import path
from . import views

urlpatterns = [
    path("", views.contratos_list, name="contratos_list"),
    path("crear/", views.contrato_crear, name="contrato_crear"),
    path("editar/<int:id>/", views.contrato_editar, name="contrato_editar"),
    path("eliminar/<int:id>/", views.contrato_eliminar, name="contrato_eliminar"),
    path("<int:id>/", views.contrato_detalle, name="contrato_detalle"),

    # Entregas
    path("<int:contrato_id>/entrega/crear/", views.entrega_crear, name="entrega_crear"),
    path("entrega/editar/<int:id>/", views.entrega_editar, name="entrega_editar"),
]
