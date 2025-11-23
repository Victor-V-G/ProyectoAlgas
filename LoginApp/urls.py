from django.urls import path
from .views import RenderLoginForm, RenderLogout

# ===============================================================
# LoginApp/urls.py
#
# Rutas correspondientes al módulo de autenticación.
#
# Incluye:
#   - Pantalla de login
#   - Cierre de sesión (logout)
#
# Estas rutas son usadas por los decoradores y por el flujo de
# autenticación general del sistema.
# ===============================================================
urlpatterns = [

    # -----------------------------------------------------------
    # RUTA PRINCIPAL DE LOGIN
    #
    # URL:
    #    /login/   (o / si está montado como root)
    #
    # Vista:
    #    RenderLoginForm
    #
    # Name:
    #    "Login"
    #
    # Esta vista:
    #   - muestra el formulario de login (GET)
    #   - procesa autenticación (POST)
    # -----------------------------------------------------------
    path("", RenderLoginForm, name="Login"),

    # -----------------------------------------------------------
    # LOGOUT DEL SISTEMA
    #
    # URL:
    #    /logout/
    #
    # Vista:
    #    RenderLogout
    #
    # Name:
    #    "logout"
    #
    # Esta vista:
    #   - limpia la sesión
    #   - registra auditoría (decorador)
    #   - redirige al formulario de login
    # -----------------------------------------------------------
    path("logout/", RenderLogout, name="logout"),
]
