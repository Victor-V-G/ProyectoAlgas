# ===============================================================
# StockApp/views.py
# Vistas para la gestión del stock de Maxisacos en el sistema.
#
# Incluye:
# - Listado de registros
# - Creación
# - Edición
# - Eliminación
# - Detalle
#
# Se utilizan:
# - Decoradores de permisos (requiere_permiso)
# - Decorador de auditoría (auditar)
# - Formularios Django
# - Mensajes del framework (Django messages)
# ===============================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from UsuariosApp.models import UsuariosModels
from .models import Maxisaco
from .forms import MaxisacoForm
from AuditoriaApp.decorators import auditar
from RolApp.decorators import requiere_permiso


# ===============================================================
# FUNCIÓN AUXILIAR: obtener usuario desde la sesión
#
# - Lee la variable "Usuario_Ingresado" guardada en la sesión.
# - Devuelve el usuario asociado o None si no existe.
# - Se usa para llenar campos auditables (registrado_por, actualizado_por).
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
# LISTAR STOCK
#
# Decoradores:
#   @requiere_permiso("PermisoEditarStock")
#      → valida que el usuario tenga permiso para gestionar stock.
#
# Lógica:
#   - Obtiene todos los Maxisacos ordenados por fecha descendente.
#   - Renderiza la lista.
# ===============================================================
@requiere_permiso("PermisoEditarStock")
def stock_list(request):
    maxisacos = Maxisaco.objects.all().order_by("-fecha_registro")
    return render(request, "stock/lista.html", {"maxisacos": maxisacos})


# ===============================================================
# CREAR STOCK
#
# Decoradores:
#   @requiere_permiso("PermisoEditarStock")
#      → exige permisos para crear stock.
#
#   @auditar("crear", "Stock", mensaje)
#      → registra automáticamente en auditoría la acción realizada.
#
# Lógica:
#   - Si el método es POST: procesa formulario.
#   - Si es válido: asigna usuario que registra y actualiza.
#   - Guarda registro, envía mensaje y redirige.
# ===============================================================
@requiere_permiso("PermisoEditarStock")
@auditar(
    "crear",
    "Stock",
    lambda req, *a, **k: f"Creado Maxisaco para especie {req.POST.get('especie')} "
                         f"con {req.POST.get('peso_kg')} kg"
)
def stock_crear(request):
    usuario = get_user_from_session(request)

    if request.method == "POST":
        form = MaxisacoForm(request.POST)

        if form.is_valid():
            m = form.save(commit=False)  # Se detiene para asignar campos extra
            m.registrado_por = usuario
            m.actualizado_por = usuario
            m.save()

            messages.success(request, "Registro de stock agregado.")
            return redirect("stock")

    else:
        form = MaxisacoForm()

    return render(request, "stock/crear.html", {"form": form})


# ===============================================================
# EDITAR STOCK
#
# Decoradores:
#   @requiere_permiso("PermisoEditarStock")
#   @auditar("editar", "Stock", mensaje_dinamico)
#
# Lógica:
#   - Obtiene el Maxisaco por ID (404 si no existe)
#   - Si el método es POST: valida el formulario y guarda cambios.
#   - Actualiza "actualizado_por".
# ===============================================================
@requiere_permiso("PermisoEditarStock")
@auditar(
    "editar",
    "Stock",
    lambda req, *a, **k: f"Editado Maxisaco ID {k['id']}"
)
def stock_editar(request, id):
    usuario = get_user_from_session(request)
    m = get_object_or_404(Maxisaco, id=id)

    if request.method == "POST":
        form = MaxisacoForm(request.POST, instance=m)

        if form.is_valid():
            maxisaco = form.save(commit=False)
            maxisaco.actualizado_por = usuario
            maxisaco.save()

            messages.success(request, "Registro actualizado.")
            return redirect("stock")

    else:
        form = MaxisacoForm(instance=m)

    return render(request, "stock/editar.html", {"form": form, "maxisaco": m})


# ===============================================================
# ELIMINAR STOCK
#
# Decoradores:
#   @requiere_permiso("PermisoEditarStock")
#   @auditar("eliminar", "Stock", mensaje)
#
# Lógica:
#   - Busca el Maxisaco por ID.
#   - Lo elimina
#   - Muestra mensaje de confirmación.
# ===============================================================
@requiere_permiso("PermisoEditarStock")
@auditar(
    "eliminar",
    "Stock",
    lambda req, *a, **k: f"Eliminado Maxisaco ID {k['id']}"
)
def stock_eliminar(request, id):
    m = get_object_or_404(Maxisaco, id=id)
    m.delete()

    messages.success(request, "Registro eliminado.")
    return redirect("stock")


# ===============================================================
# DETALLE DE UN REGISTRO DE STOCK
#
# Decoradores:
#   @requiere_permiso("PermisoEditarStock")
#
# Lógica:
#   - Obtiene el Maxisaco por ID.
#   - Lo muestra en una plantilla de detalle.
# ===============================================================
@requiere_permiso("PermisoEditarStock")
def stock_detalle(request, id):
    m = get_object_or_404(Maxisaco, id=id)
    return render(request, "stock/detalle.html", {"m": m})
