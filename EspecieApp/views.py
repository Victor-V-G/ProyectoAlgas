from django.shortcuts import render
from RolApp.decorators import requiere_permiso

# Core Django utilities
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# Modelos y formularios del módulo
from .models import Especie
from .forms import EspecieForm

# Auditoría
from AuditoriaApp.decorators import auditar


# ===============================================================
# MÓDULO: EspecieApp — VISTAS CRUD PARA ESPECIES DE ALGAS
#
# Este módulo permite:
#   - Listar especies
#   - Crear nuevas especies
#   - Editar especies existentes
#   - Eliminar especies
#   - Ver detalles
#
# Todas las vistas están protegidas con:
#   @requiere_permiso("PermisoEditarStock")
#     → Solo usuarios con permiso pueden administrar especies
#
# Y además, operaciones sensibles registran auditoría:
#   @auditar("crear" / "editar" / "eliminar", ...)
# ===============================================================


# ===============================================================
# LISTADO DE ESPECIES
#
# Decorador:
#   @requiere_permiso("PermisoEditarStock")
#
# Función:
#   - Obtiene todas las especies ordenadas alfabéticamente
#   - Renderiza lista.html
# ===============================================================
@requiere_permiso("PermisoEditarStock")
def especies_list(request):
    especies = Especie.objects.all().order_by("nombre")
    return render(request, "especies/lista.html", {"especies": especies})


# ===============================================================
# CREAR ESPECIE
#
# Decoradores:
#   @requiere_permiso("PermisoEditarStock")
#   @auditar("crear", "Especie", mensaje dinámico)
#
# Flujo:
#   - Si es GET → formulario vacío
#   - Si es POST:
#       * validar formulario
#       * guardar registro
#       * mostrar mensaje de éxito
#       * redirigir
# ===============================================================
@requiere_permiso("PermisoEditarStock")
@auditar("crear", "Especie", lambda req, *a, **k: f"Creada especie '{req.POST.get('nombre')}'")
def especie_crear(request):

    if request.method == "POST":
        form = EspecieForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Especie creada.")
            return redirect("especies")

    else:
        form = EspecieForm()

    return render(request, "especies/crear.html", {"form": form})


# ===============================================================
# EDITAR ESPECIE
#
# Decoradores:
#   @requiere_permiso("PermisoEditarStock")
#   @auditar("editar", "Especie", mensaje dinámico)
#
# Flujo:
#   1) Obtener especie por ID (404 si no existe)
#   2) Si es GET → formulario precargado
#   3) Si es POST → validar y actualizar
#   4) Registrar auditoría
#   5) Redirigir con mensaje
# ===============================================================
@requiere_permiso("PermisoEditarStock")
@auditar("editar", "Especie", lambda req, *a, **k: f"Editada especie ID {k['id']}")
def especie_editar(request, id):

    especie = get_object_or_404(Especie, id=id)

    if request.method == "POST":
        form = EspecieForm(request.POST, instance=especie)

        if form.is_valid():
            form.save()
            messages.success(request, "Especie actualizada.")
            return redirect("especies")

    else:
        form = EspecieForm(instance=especie)

    return render(request, "especies/editar.html", {
        "form": form,
        "especie": especie,
    })


# ===============================================================
# ELIMINAR ESPECIE
#
# Decoradores:
#   @requiere_permiso("PermisoEditarStock")
#   @auditar("eliminar", "Especie", mensaje dinámico)
#
# Flujo:
#   - Obtener especie
#   - Eliminar registro
#   - Registrar auditoría
#   - Redirigir con mensaje
# ===============================================================
@requiere_permiso("PermisoEditarStock")
@auditar("eliminar", "Especie", lambda req, *a, **k: f"Eliminada especie ID {k['id']}")
def especie_eliminar(request, id):

    especie = get_object_or_404(Especie, id=id)
    especie.delete()

    messages.success(request, "Especie eliminada.")
    return redirect("especies")


# ===============================================================
# DETALLE DE ESPECIE
#
# Decorador:
#   @requiere_permiso("PermisoEditarStock")
#
# Función:
#   - Obtiene la especie solicitada
#   - Renderiza detalle.html
# ===============================================================
@requiere_permiso("PermisoEditarStock")
def especie_detalle(request, id):
    especie = get_object_or_404(Especie, id=id)
    return render(request, "especies/detalle.html", {"especie": especie})
