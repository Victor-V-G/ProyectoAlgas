# ===============================================================
# RolApp/decorators.py
#
# Decorador: @requiere_permiso
#
# Permite restringir el acceso a vistas según el rol asignado
# al usuario y los permisos definidos dentro del modelo RolModels.
#
# Flujo general:
#   1. Verifica si el usuario está en sesión.
#   2. Obtiene al usuario y su rol.
#   3. Revisa si el rol tiene el permiso requerido.
#   4. Si NO lo tiene → bloquea acceso, muestra mensaje,
#      y redirige según el rol.
#
# Uso en vistas:
#     @requiere_permiso("PermisoEditarStock")
#     def stock_list(request):
#         ...
#
# ===============================================================

from django.shortcuts import redirect
from django.contrib import messages
from UsuariosApp.models import UsuariosModels


# ===============================================================
# DECORADOR PRINCIPAL: requiere_permiso(nombre_permiso)
#
# Parámetro:
#   - nombre_permiso: string con el nombre del campo booleano
#     dentro del modelo RolModels (ej: "PermisoEditarStock").
#
# Retorna:
#   - decorator → que envuelve la vista
# ===============================================================
def requiere_permiso(nombre_permiso):

    # -----------------------------------------------------------
    # decorator(view_func)
    #   - Recibe la función de vista que será protegida.
    # -----------------------------------------------------------
    def decorator(view_func):

        # -------------------------------------------------------
        # wrapper()
        #   - Función que reemplaza temporalmente a la vista real.
        #   - Realiza validaciones antes de ejecutar la vista.
        # -------------------------------------------------------
        def wrapper(request, *args, **kwargs):

            # ===================================================
            # 1. VALIDAR QUE EL USUARIO ESTÉ EN SESIÓN
            # ===================================================
            username = request.session.get('Usuario_Ingresado')

            if not username:
                messages.error(request, "Debes iniciar sesión.")
                return redirect('Login')

            # ===================================================
            # 2. INTENTAR OBTENER EL USUARIO Y SU ROL
            # ===================================================
            try:
                # select_related("Rol"):
                #   → optimiza consulta usando join
                usuario = UsuariosModels.objects.select_related("Rol").get(Username=username)
            except UsuariosModels.DoesNotExist:
                messages.error(request, "Usuario inválido.")
                return redirect('Login')

            rol = usuario.Rol

            # Si el usuario no tiene un rol asociado
            if not rol:
                messages.error(request, "Tu cuenta no tiene un rol asignado.")
                return redirect('Login')

            # ===================================================
            # 3. VALIDACIÓN DEL PERMISO
            #
            # getattr(rol, nombre_permiso, False):
            #   → Obtiene el valor del permiso (True/False).
            #   → Si no existe el atributo, devuelve False.
            # ===================================================
            if not getattr(rol, nombre_permiso, False):
                messages.error(request, "No tienes permisos para acceder aquí.")

                # --------------------------------------------------
                # Redirección personalizada según el tipo de rol
                # para enviarlo a su área correspondiente.
                # --------------------------------------------------
                if rol.NombreRol in ["RolAdmin", "Gerente"]:
                    return redirect("dashboard")

                elif rol.NombreRol == "EncargadoStock":
                    return redirect("stock")

                elif rol.NombreRol == "Operario":
                    return redirect("especies")

                # Si no calza con ningún rol → fallback general
                return redirect("Login")

            # ===================================================
            # 4. SI TODO ES VÁLIDO → EJECUTA LA VISTA ORIGINAL
            # ===================================================
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
