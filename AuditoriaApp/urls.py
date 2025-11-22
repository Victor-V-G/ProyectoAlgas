from django.urls import path
from . import views

urlpatterns = [
    path("", views.auditoria_list, name="auditoria"),
    path("detalle/<int:id>/", views.auditoria_detalle, name="auditoria_detalle"),
]
