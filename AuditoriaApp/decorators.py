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

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            respuesta = view_func(request, *args, **kwargs)

            # Registrar auditoría SOLO si la operación fue exitosa:
            # Es decir, si el view hizo redirect (código 302)
            if request.method == "POST" and hasattr(respuesta, "status_code") and respuesta.status_code in (301, 302):

                # Detalle dinámico
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
