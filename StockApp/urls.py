from django.urls import path
from . import views

urlpatterns = [
    path("", views.stock_list, name="stock"),
    path("crear/", views.stock_crear, name="stock_crear"),
    path("editar/<int:id>/", views.stock_editar, name="stock_editar"),
    path("eliminar/<int:id>/", views.stock_eliminar, name="stock_eliminar"),
    path("<int:id>/", views.stock_detalle, name="stock_detalle"),
]
