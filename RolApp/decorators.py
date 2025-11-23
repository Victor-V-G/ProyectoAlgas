# RolApp/decorators.py
from django.shortcuts import redirect
from django.contrib import messages
from UsuariosApp.models import UsuariosModels


def requiere_permiso(nombre_permiso):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):

            username = request.session.get('Usuario_Ingresado')

            if not username:
                messages.error(request, "Debes iniciar sesión.")
                return redirect('Login')

            try:
                usuario = UsuariosModels.objects.select_related("Rol").get(Username=username)
            except UsuariosModels.DoesNotExist:
                messages.error(request, "Usuario inválido.")
                return redirect('Login')

            rol = usuario.Rol

            if not rol:
                messages.error(request, "Tu cuenta no tiene un rol asignado.")
                return redirect('Login')

            # =============================
            # VALIDACIÓN DEL PERMISO
            # =============================
            if not getattr(rol, nombre_permiso, False):
                messages.error(request, "No tienes permisos para acceder aquí.")

                # Redirección por rol
                if rol.NombreRol in ["RolAdmin", "Gerente"]:
                    return redirect("dashboard")

                elif rol.NombreRol == "EncargadoStock":
                    return redirect("stock")

                elif rol.NombreRol == "Operario":
                    return redirect("especies")

                return redirect("Login")

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator
