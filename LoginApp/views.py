from django.shortcuts import render, redirect
from . import forms
from UsuariosApp.models import UsuariosModels
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from AuditoriaApp.decorators import auditar
# Create your views here.

@auditar("login", "Autenticación",
         lambda req, *a, **k: f"Intento de login usuario '{req.POST.get('UsernameField')}'")
def RenderLoginForm(request):
    form = forms.LoginForm(request.POST)
    data = {'form': form}

    if request.method == "POST":
        UsernameField = request.POST['UsernameField']
        PasswordField = request.POST['PasswordField']

        # ---------- VALIDACIÓN DEL USUARIO ----------
        if not UsuariosModels.objects.filter(Username=UsernameField).exists():
            messages.error(request, "Credenciales incorrectas.")
            return render(request, 'LoginTemplate/Form.html', data)

        UsuarioRecuperado = UsuariosModels.objects.get(Username=UsernameField)

        if not check_password(PasswordField, UsuarioRecuperado.Password):
            messages.error(request, "Credenciales incorrectas.")
            return render(request, 'LoginTemplate/Form.html', data)

        # ---------- LOGIN EXITOSO ----------
        request.session['Usuario_Ingresado'] = UsuarioRecuperado.Username
        request.session['Usuario_RolId'] = UsuarioRecuperado.Rol.RolId
        request.session['Usuario_RolNombre'] = UsuarioRecuperado.Rol.NombreRol

        rol = UsuarioRecuperado.Rol

        # ============================================================
        #   REDIRECCIÓN AUTOMÁTICA SEGÚN EL NOMBRE DEL ROL (TU VERSIÓN)
        # ============================================================

        if rol.NombreRol == "RolAdmin":
            return redirect("dashboard")

        elif rol.NombreRol == "Gerente":
            return redirect("dashboard")

        elif rol.NombreRol == "EncargadoStock":
            return redirect("stock")  # tu url para stock

        elif rol.NombreRol == "Operario":
            return redirect("especies")  # o la vista que tú desees

        # Si existe el rol pero no coincide con ninguno
        messages.error(request, "Tu rol no tiene acceso a ninguna sección del sistema.")
        return render(request, 'LoginTemplate/Form.html', data)

    return render(request, 'LoginTemplate/Form.html', data)


@auditar("logout", "Autenticación", "Cierre de sesión")
def RenderLogout(request):
    request.session.flush()
    return redirect('Login')