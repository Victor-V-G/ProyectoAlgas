from django.shortcuts import render

# Utilidades Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# Modelos del módulo
from .models import Contrato, EntregaContrato

# Formularios asociados
from .forms import ContratoForm, EntregaContratoForm

# Auditoría y permisos
from AuditoriaApp.decorators import auditar
from RolApp.decorators import requiere_permiso

# Usuarios para trazabilidad
from UsuariosApp.models import UsuariosModels


# ===============================================================
# FUNCIÓN AUXILIAR:
#   Recupera el usuario actualmente logueado desde la sesión.
#
# Se utiliza para:
#   - Registrar quién crea contratos
#   - Registrar quién los edita
#   - Llenar campos de auditoría (creado_por / actualizado_por)
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
# LISTADO DE CONTRATOS
#
# Decorador:
#   @requiere_permiso("PermisoCrearContratos")
#
# Función:
#   - Lista todos los contratos en orden descendente por ID
#   - Renderiza la vista HTML correspondiente
# ===============================================================
@requiere_permiso("PermisoCrearContratos")
def contratos_list(request):
    contratos = Contrato.objects.all().order_by("-id")
    return render(request, "contratos/lista.html", {"contratos": contratos})


# ===============================================================
# CREAR CONTRATO
#
# Decoradores:
#   @requiere_permiso("PermisoCrearContratos")
#   @auditar("crear", "Contrato", mensaje dinámico)
#
# Flujo:
#   - GET → formulario vacío
#   - POST → validar formulario → registrar contrato → auditar → redirigir
#
# Auditoría:
#   Registra acción "crear" y mensaje con nombre de cliente
# ===============================================================
@requiere_permiso("PermisoCrearContratos")
@auditar("crear", "Contrato",
         lambda req, *a, **k: f"Contrato creado para cliente {req.POST.get('cliente')}")
def contrato_crear(request):

    usuario = get_user_from_session(request)

    if request.method == "POST":
        form = ContratoForm(request.POST)

        if form.is_valid():
            contrato = form.save(commit=False)
            contrato.creado_por = usuario
            contrato.actualizado_por = usuario
            contrato.save()

            messages.success(request, "Contrato creado exitosamente.")
            return redirect("contratos")

    else:
        form = ContratoForm()

    return render(request, "contratos/crear.html", {"form": form})


# ===============================================================
# EDITAR CONTRATO
#
# Decoradores:
#   @requiere_permiso("PermisoCrearContratos")
#   @auditar("editar", "Contrato", mensaje dinámico)
#
# Flujo:
#   - Obtiene contrato por ID
#   - GET → cargar datos
#   - POST → validar formulario → actualizar → auditar → redirigir
# ===============================================================
@requiere_permiso("PermisoCrearContratos")
@auditar("editar", "Contrato",
         lambda req, *a, **k: f"Contrato ID {k['id']} editado")
def contrato_editar(request, id):

    usuario = get_user_from_session(request)
    contrato = get_object_or_404(Contrato, id=id)

    if request.method == "POST":
        form = ContratoForm(request.POST, instance=contrato)

        if form.is_valid():
            contrato = form.save(commit=False)
            contrato.actualizado_por = usuario
            contrato.save()

            messages.success(request, "Contrato actualizado.")
            return redirect("contratos")

    else:
        form = ContratoForm(instance=contrato)

    return render(request, "contratos/editar.html", {
        "form": form,
        "contrato": contrato
    })


# ===============================================================
# ELIMINAR CONTRATO
#
# Decoradores:
#   @requiere_permiso("PermisoCrearContratos")
#   @auditar("eliminar", "Contrato", mensaje dinámico)
#
# Flujo:
#   - Obtener contrato
#   - Eliminar registro
#   - Registrar auditoría
#   - Redirigir con mensaje
# ===============================================================
@requiere_permiso("PermisoCrearContratos")
@auditar("eliminar", "Contrato",
         lambda req, *a, **k: f"Contrato ID {k['id']} eliminado")
def contrato_eliminar(request, id):

    contrato = get_object_or_404(Contrato, id=id)
    contrato.delete()

    messages.success(request, "Contrato eliminado.")
    return redirect("contratos")


# ===============================================================
# DETALLE DE CONTRATO
#
# Decorador:
#   @requiere_permiso("PermisoCrearContratos")
#
# Función:
#   - Obtiene contrato por ID
#   - Obtiene todas sus entregas (relación inversa: contrato.entregas)
#   - Renderiza la vista detalle.html
# ===============================================================
@requiere_permiso("PermisoCrearContratos")
def contrato_detalle(request, id):

    contrato = get_object_or_404(Contrato, id=id)
    entregas = contrato.entregas.all().order_by("mes")

    return render(request, "contratos/detalle.html", {
        "contrato": contrato,
        "entregas": entregas
    })


# ===============================================================
# CREAR ENTREGA DE CONTRATO
#
# Decoradores:
#   @requiere_permiso("PermisoCrearContratos")
#   @auditar("crear", "Entrega Contrato", mensaje dinámico)
#
# Flujo:
#   - GET → formulario vacío
#   - POST → validar formulario → asociar entrega al contrato
#   - Registrar auditoría
#   - Redirigir al detalle del contrato
# ===============================================================
@requiere_permiso("PermisoCrearContratos")
@auditar("crear", "Entrega Contrato",
         lambda req, *a, **k: f"Nueva entrega agregada al contrato {k['contrato_id']}")
def entrega_crear(request, contrato_id):

    contrato = get_object_or_404(Contrato, id=contrato_id)

    if request.method == "POST":
        form = EntregaContratoForm(request.POST)

        if form.is_valid():
            entrega = form.save(commit=False)
            entrega.contrato = contrato
            entrega.save()

            messages.success(request, "Entrega agregada.")
            return redirect("contrato_detalle", id=contrato_id)

    else:
        form = EntregaContratoForm()

    return render(request, "contratos/crear_entrega.html", {
        "form": form,
        "contrato": contrato
    })


# ===============================================================
# EDITAR ENTREGA DE CONTRATO
#
# Decorador:
#   @requiere_permiso("PermisoCrearContratos")
#
# Flujo:
#   - Obtener entrega por ID
#   - GET → cargar datos
#   - POST → validar y actualizar
#   - Redirigir a detalle del contrato
# ===============================================================
@requiere_permiso("PermisoCrearContratos")
def entrega_editar(request, id):

    entrega = get_object_or_404(EntregaContrato, id=id)

    if request.method == "POST":
        form = EntregaContratoForm(request.POST, instance=entrega)

        if form.is_valid():
            form.save()

            messages.success(request, "Entrega actualizada.")
            return redirect("contrato_detalle", id=entrega.contrato.id)

    else:
        form = EntregaContratoForm(instance=entrega)

    return render(request, "contratos/editar_entrega.html", {
        "form": form,
        "entrega": entrega
    })
