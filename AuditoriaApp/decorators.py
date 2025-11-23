from functools import wraps
from AuditoriaApp.utils import registrar_auditoria
from UsuariosApp.models import UsuariosModels


# ===============================================================
# FUNCIÓN AUXILIAR: get_user_from_session
#
# Obtiene el usuario actualmente logueado mediante el nombre
# de usuario almacenado en la sesión.
#
# Retorna:
#   - instancia de UsuariosModels si existe
#   - None si no hay usuario o no existe en BD
#
# NOTA:
#   Esta función no registra auditoría por sí sola.
# ===============================================================
def get_user_from_session(request):
    username = request.session.get("Usuario_Ingresado")

    if not username:
        return None

    try:
        return UsuariosModels.objects.get(Username=username)
    except UsuariosModels.DoesNotExist:
        return None


# ===============================================================
# DECORADOR: auditar
#
# Permite registrar automáticamente acciones de auditoría para
# cualquier vista que lo utilice. Es uno de los componentes
# centrales del sistema de trazabilidad.
#
# Parámetros:
#   accion  → tipo de operación (crear, editar, eliminar, login…)
#   modulo  → nombre del módulo afectado (Stock, Contrato, Insumos…)
#   detalle → texto o función para generar detalle dinámico
#
# Comportamiento:
#   - Envuelve la vista original.
#   - Ejecuta la vista.
#   - *Solo si la vista responde con un redirect (302/301)*
#     se registra la auditoría.
#
# ¿Por qué solo registrar en redirect?
#   Porque un redirect indica que la operación fue EXITOSA.
#   Ejemplos:
#       • Crear → redirect al listado
#       • Editar → redirect al listado
#       • Eliminar → redirect al listado
#
#   Si la vista devuelve render() significa que hubo error
#   de validación → NO debe registrarse auditoría.
#
# Detalle dinámico:
#   - Si “detalle” es función → se ejecuta pasando request y args
#   - Si es string → se usa directamente
#
# Este diseño permite registrar mensajes como:
#   "Editado Maxisaco ID 21"
#   "Creado contrato para cliente Juan Pérez"
# ===============================================================
def auditar(accion, modulo, detalle=None):

    def decorator(view_func):

        @wraps(view_func)  # preserva nombre, docstring y metadata
        def wrapper(request, *args, **kwargs):

            # ---------------------------------------------------
            # Ejecutar la vista original y obtener la respuesta
            # ---------------------------------------------------
            respuesta = view_func(request, *args, **kwargs)

            # ---------------------------------------------------
            # Registrar auditoría SOLO SI:
            #   1. El método es POST (acciones que modifican datos)
            #   2. La vista devolvió un redirect (301 o 302)
            # ---------------------------------------------------
            if (
                request.method == "POST"
                and hasattr(respuesta, "status_code")
                and respuesta.status_code in (301, 302)
            ):

                # -----------------------------------------------
                # Generar detalle dinámico si se entregó una función
                # -----------------------------------------------
                if callable(detalle):
                    valor_detalle = detalle(request, *args, **kwargs)
                else:
                    valor_detalle = detalle

                # -----------------------------------------------
                # Registrar finalmente la auditoría
                # -----------------------------------------------
                registrar_auditoria(
                    request=request,
                    accion=accion,
                    modulo=modulo,
                    detalle=valor_detalle
                )

            # ---------------------------------------------------
            # Devolver la respuesta original de la vista
            # ---------------------------------------------------
            return respuesta

        return wrapper

    return decorator
