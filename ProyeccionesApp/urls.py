# ProyeccionesApp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("actualizar/", views.actualizar_proyecciones, name="proyecciones_actualizar"),
]