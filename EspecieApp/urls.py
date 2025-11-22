from django.urls import path
from . import views

urlpatterns = [
    path("", views.especies_list, name="especies"),
    path("crear/", views.especie_crear, name="especie_crear"),
    path("editar/<int:id>/", views.especie_editar, name="especie_editar"),
    path("eliminar/<int:id>/", views.especie_eliminar, name="especie_eliminar"),
    path("<int:id>/", views.especie_detalle, name="especie_detalle"),
]
