# ===============================================================
# InsumoApp/views.py
#
# Vistas del módulo de Insumos.
# Permiten:
#   - Listar insumos
#   - Crear insumos
#   - Editar insumos
#   - Eliminar insumos
#   - Ver detalle de insumos
#
# Todas las vistas requieren permisos de edición de stock
# ya que el módulo es parte de la gestión operativa.
#
# Incluye auditoría automática para:
#   - crear
#   - editar
#   - eliminar
#
# El usuario autenticado se obtiene desde sesión
# mediante get_user_from_session().
# ===============================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from UsuariosApp.models import UsuariosModels
from .models import Insumo
from .forms import InsumoForm
from AuditoriaApp.decorators import auditar
from RolApp.decorators import requiere_permiso


# ===============================================================
# FUNCIÓN AUXILIAR: obtener el usuario desde la sesión
#
# Retorna:
#   - objeto UsuariosModels si existe
#   - None si no hay sesión o no coincide usuario
#
# Se usa para completar los campos:
#   - creado_por
#   - actualizado_por
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
# LISTAR INSUMOS
#
# Decorador:
#   @requiere_permiso("PermisoEditarStock")
#     → Solo usuarios con este permiso pueden acceder.
#
# Lógica:
#   - Obtiene todos los insumos ordenados alfabéticamente.
#   - Renderiza el template de lista.
# ===============================================================
@requiere_permiso("PermisoEditarStock")
def insumos_list(request):
    insumos = Insumo.objects.all().order_by("nombre")
    return render(request, "insumos/lista.html", {"insumos": insumos})


# ===============================================================
# CREAR INSUMO
#
# Decoradores:
#   @requiere_permiso("PermisoEditarStock")
#     → Controla acceso según permisos del rol.
#
#   @auditar("crear", "Insumos", mensaje)
#     → Registra en auditoría quién creó qué insumo.
#
# Flujo:
#   - Si es POST:
#       * validar formulario
#       * asignar creado_por / actualizado_por
#       * guardar
#       * mostrar mensaje
#       * redirigir
#   - Si es GET:
#       * mostrar formulario vacío
# ===============================================================
@requiere_permiso("PermisoEditarStock")
@auditar(
    "crear",
    "Insumos",
    lambda req, *a, **k: f"Creado insumo '{req.POST.get('nombre')}'"
)
def insumo_crear(request):

    usuario = get_user_from_session(request)

    if request.method == "POST":
        form = InsumoForm(request.POST)

        if form.is_valid():
            insumo = form.save(commit=False)
            insumo.creado_por = usuario
            insumo.actualizado_por = usuario
            insumo.save()

            messages.success(request, "Insumo registrado.")
            return redirect("insumos")
    else:
        form = InsumoForm()

    return render(request, "insumos/crear.html", {"form": form})


# ===============================================================
# EDITAR INSUMO
#
# Decoradores:
#   @requiere_permiso("PermisoEditarStock")
#   @auditar("editar", "Insumos", mensaje_dinámico)
#
# Flujo:
#   - Obtener insumo por ID
#   - Si es POST → validar y guardar cambios
#   - Actualizar actualizado_por
#   - Mostrar mensaje de éxito
# ===============================================================
@requiere_permiso("PermisoEditarStock")
@auditar(
    "editar",
    "Insumos",
    lambda req, *a, **k: f"Insumo ID {k['id']} editado"
)
def insumo_editar(request, id):

    usuario = get_user_from_session(request)
    insumo = get_object_or_404(Insumo, id=id)

    if request.method == "POST":
        form = InsumoForm(request.POST, instance=insumo)

        if form.is_valid():
            insumo = form.save(commit=False)
            insumo.actualizado_por = usuario
            insumo.save()

            messages.success(request, "Insumo actualizado.")
            return redirect("insumos")
    else:
        form = InsumoForm(instance=insumo)

    return render(request, "insumos/editar.html", {"form": form, "insumo": insumo})


# ===============================================================
# ELIMINAR INSUMO
#
# Decoradores:
#   @requiere_permiso("PermisoEditarStock")
#   @auditar("eliminar", "Insumos", mensaje)
#
# Flujo:
#   - Obtener insumo
#   - Eliminarlo
#   - Registrar auditoría
#   - Redirigir y mostrar mensaje
# ===============================================================
@requiere_permiso("PermisoEditarStock")
@auditar(
    "eliminar",
    "Insumos",
    lambda req, *a, **k: f"Insumo ID {k['id']} eliminado"
)
def insumo_eliminar(request, id):

    insumo = get_object_or_404(Insumo, id=id)
    insumo.delete()

    messages.success(request, "Insumo eliminado.")
    return redirect("insumos")


# ===============================================================
# DETALLE DE INSUMO
#
# Decorador:
#   @requiere_permiso("PermisoEditarStock")
#
# Flujo:
#   - Obtiene insumo por ID
#   - Renderiza plantilla de detalle
# ===============================================================
@requiere_permiso("PermisoEditarStock")
def insumo_detalle(request, id):
    insumo = get_object_or_404(Insumo, id=id)
    return render(request, "insumos/detalle.html", {"insumo": insumo})
