from .models import Auditoria
from UsuariosApp.models import UsuariosModels

def registrar_auditoria(request, accion, modulo, detalle=""):
    username = request.session.get("Usuario_Ingresado")

    usuario = None
    if username:
        try:
            usuario = UsuariosModels.objects.get(Username=username)
        except UsuariosModels.DoesNotExist:
            usuario = None

    Auditoria.objects.create(
        usuario=usuario,
        accion=accion,
        modulo=modulo,
        detalle=detalle
    )
