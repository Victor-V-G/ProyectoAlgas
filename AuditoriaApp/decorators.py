from functools import wraps
from AuditoriaApp.utils import registrar_auditoria
from UsuariosApp.models import UsuariosModels


def get_user_from_session(request):
    username = request.session.get("Usuario_Ingresado")
    if not username:
        return None
    try:
        return UsuariosModels.objects.get(Username=username)
    except UsuariosModels.DoesNotExist:
        return None


def auditar(accion, modulo, detalle=None):
    """
    Decorador universal para registrar automáticamente auditoría.

    Ejemplo:
        @auditar("crear", "Especie")
        def especie_crear(...):
            ...

    Parametros:
        accion  -> "crear", "editar", "eliminar", "login", etc.
        modulo  -> "Stock", "Insumo", "Contrato", etc.
        detalle -> puede ser string estático o una función que recibe (request, args, kwargs)
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            respuesta = view_func(request, *args, **kwargs)

            # Caso detalle dinámico
            if callable(detalle):
                valor_detalle = detalle(request, *args, **kwargs)
            else:
                valor_detalle = detalle

            registrar_auditoria(
                request=request,
                accion=accion,
                modulo=modulo,
                detalle=valor_detalle
            )

            return respuesta
        return wrapper
    return decorator
