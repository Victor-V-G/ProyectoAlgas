# ===============================================================
# ProyeccionesApp/urls.py
#
# Define las rutas asociadas a la funcionalidad de proyecciones.
#
# Actualmente solo expone una ruta:
#   - actualizar/ → ejecuta el proceso de recalcular proyecciones
#
# Estas rutas son usadas desde el dashboard mediante un botón:
#   <a href="{% url 'proyecciones_actualizar' %}">
# ===============================================================

from django.urls import path
from . import views

urlpatterns = [

    # -----------------------------------------------------------
    # ACTUALIZAR PROYECCIONES
    #
    # URL:
    #   /proyecciones/actualizar/
    #
    # Vista:
    #   views.actualizar_proyecciones
    #
    # Name (para uso en templates):
    #   "proyecciones_actualizar"
    #
    # Esta ruta permite ejecutar el microservicio que recalcula
    # las proyecciones ejecutivas.
    # -----------------------------------------------------------
    path("actualizar/", views.actualizar_proyecciones, name="proyecciones_actualizar"),
]
