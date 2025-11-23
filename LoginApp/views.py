from django.shortcuts import render, redirect
from . import forms
from UsuariosApp.models import UsuariosModels
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from AuditoriaApp.decorators import auditar


# ================================================================
# VISTA DE LOGIN — RenderLoginForm
#
# Decorador:
#   @auditar("login", "Autenticación", mensaje dinámico)
#
#   Registra en la auditoría:
#       - Que se intentó realizar un login
#       - El nombre ingresado (aunque sea incorrecto)
#
# Flujo de la vista:
#   1. Carga el formulario.
#   2. Si el método es POST → validar credenciales.
#   3. Si usuario no existe → error.
#   4. Si contraseña incorrecta → error.
#   5. Si credenciales correctas → guardar datos en sesión.
#   6. Redirigir según el rol del usuario.
# ================================================================
@auditar(
    "login",
    "Autenticación",
    lambda req, *a, **k: f"Intento de login usuario '{req.POST.get('UsernameField')}'"
)
def RenderLoginForm(request):

    # Formulario cargado con los datos del POST (si los hay)
    form = forms.LoginForm(request.POST)
    data = {'form': form}

    # ------------------------------------------------------------
    # SI LA SOLICITUD ES POST → PROCESAR LOGIN
    # ------------------------------------------------------------
    if request.method == "POST":

        UsernameField = request.POST['UsernameField']
        PasswordField = request.POST['PasswordField']

        # ========================================================
        # VALIDACIÓN 1: EL USUARIO EXISTE?
        # ========================================================
        if not UsuariosModels.objects.filter(Username=UsernameField).exists():
            messages.error(request, "Credenciales incorrectas.")
            return render(request, 'LoginTemplate/Form.html', data)

        # Recuperar usuario
        UsuarioRecuperado = UsuariosModels.objects.get(Username=UsernameField)

        # ========================================================
        # VALIDACIÓN 2: CONTRASEÑA CORRECTA?
        # check_password:
        #   → compara contraseña en texto plano con el hash guardado
        # ========================================================
        if not check_password(PasswordField, UsuarioRecuperado.Password):
            messages.error(request, "Credenciales incorrectas.")
            return render(request, 'LoginTemplate/Form.html', data)

        # ========================================================
        # LOGIN EXITOSO:
        #   - Guardar usuario en la sesión
        #   - Guardar información del rol
        #   - Usado por decoradores como @requiere_permiso
        # ========================================================
        request.session['Usuario_Ingresado'] = UsuarioRecuperado.Username
        request.session['Usuario_RolId'] = UsuarioRecuperado.Rol.RolId
        request.session['Usuario_RolNombre'] = UsuarioRecuperado.Rol.NombreRol

        rol = UsuarioRecuperado.Rol

        # ========================================================
        # REDIRECCIÓN SEGÚN EL ROL DEL USUARIO
        #
        # Esto permite que cada perfil ingrese al área que le
        # corresponde dentro del sistema.
        # ========================================================
        if rol.NombreRol == "RolAdmin":
            return redirect("dashboard")

        elif rol.NombreRol == "Gerente":
            return redirect("dashboard")

        elif rol.NombreRol == "EncargadoStock":
            return redirect("stock")

        elif rol.NombreRol == "Operario":
            return redirect("especies")

        # ========================================================
        # SI EL ROL EXISTE PERO NO TIENE RUTAS DEFINIDAS
        # ========================================================
        messages.error(request, "Tu rol no tiene acceso a ninguna sección del sistema.")
        return render(request, 'LoginTemplate/Form.html', data)

    # ------------------------------------------------------------
    # SI LA SOLICITUD ES GET → SOLO MOSTRAR EL FORMULARIO
    # ------------------------------------------------------------
    return render(request, 'LoginTemplate/Form.html', data)



# ================================================================
# VISTA DE LOGOUT — RenderLogout
#
# Decorador:
#   @auditar("logout", "Autenticación", "Cierre de sesión")
#
# Flujo:
#   1. Limpia la sesión completa (request.session.flush())
#   2. Redirige a pantalla de login
#
# Se usa para cerrar sesión de manera segura.
# ================================================================
@auditar("logout", "Autenticación", "Cierre de sesión")
def RenderLogout(request):
    # Eliminar todo lo almacenado en la sesión
    request.session.flush()

    # Regresar al login
    return redirect('Login')
