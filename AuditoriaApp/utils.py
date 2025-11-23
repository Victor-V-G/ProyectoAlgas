from .models import Auditoria
from UsuariosApp.models import UsuariosModels


# ===============================================================
# FUNCIÓN: registrar_auditoria
#
# Responsabilidad:
#   Registrar manualmente un evento de auditoría en la base de datos.
#
# Cuándo se usa:
#   - En operaciones que no utilizan el decorador @auditar
#   - Cuando una acción específica del sistema debe registrarse
#     de forma explícita desde una vista u otro servicio.
#
# Parámetros:
#   request → HttpRequest
#       Necesario para obtener el usuario logueado desde la sesión.
#
#   accion → str
#       Tipo de acción ejecutada (ej: "crear", "editar", "eliminar",
#       "login", "logout", “importar_datos"...)
#
#   modulo → str
#       Módulo o sección del sistema donde ocurrió la acción.
#       Ejemplos:
#         "Stock", "Usuarios", "Contrato", "Insumos"
#
#   detalle → str (opcional)
#       Texto descriptivo que amplía información de la acción,
#       por ejemplo:
#         "Se creó el insumo 'Yodo'"
#         "Edición de contrato ID 12"
#
# Funcionamiento interno:
#   1. Obtiene el Username desde la sesión.
#   2. Intenta recuperar el objeto UsuariosModels asociado.
#   3. Si el usuario no existe (no debería ocurrir), almacena None.
#   4. Crea un registro en la tabla Auditoria.
#
# El modelo Auditoria se encarga de almacenar:
#   - usuario (FK)
#   - acción realizada
#   - módulo afectado
#   - detalle del evento
#   - fecha/hora automática del sistema
#
# ===============================================================
def registrar_auditoria(request, accion, modulo, detalle=""):
    username = request.session.get("Usuario_Ingresado")

    usuario = None
    if username:
        try:
            usuario = UsuariosModels.objects.get(Username=username)
        except UsuariosModels.DoesNotExist:
            usuario = None

    Auditoria.objects.create(
        usuario=usuario,  # FK hacia usuario que realizó la acción
        accion=accion,    # tipo de operación ("crear", "editar"...)
        modulo=modulo,    # módulo afectado
        detalle=detalle   # mensaje descriptivo opcional
    )
