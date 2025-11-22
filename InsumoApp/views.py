from django.shortcuts import render

# Create your views here.
# utils.py dentro de InsumoApp
from UsuariosApp.models import UsuariosModels
from AuditoriaApp.decorators import auditar

def get_user_from_session(request):
    username = request.session.get("Usuario_Ingresado")
    if not username:
        return None

    try:
        return UsuariosModels.objects.get(Username=username)
    except UsuariosModels.DoesNotExist:
        return None


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Insumo
from .forms import InsumoForm


def insumos_list(request):
    insumos = Insumo.objects.all().order_by("nombre")
    return render(request, "insumos/lista.html", {"insumos": insumos})

@auditar(
    accion="crear",
    modulo="Insumos",
    detalle=lambda req, *a, **k: f"Creado insumo '{req.POST.get('nombre')}'"
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

@auditar(
    accion="editar",
    modulo="Insumos",
    detalle=lambda req, *a, **k: f"Insumo ID {k['id']} editado"
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


@auditar(
    accion="eliminar",
    modulo="Insumos",
    detalle=lambda req, *a, **k: f"Insumo ID {k['id']} eliminado"
)
def insumo_eliminar(request, id):
    insumo = get_object_or_404(Insumo, id=id)
    insumo.delete()
    messages.success(request, "Insumo eliminado.")
    return redirect("insumos")


def insumo_detalle(request, id):
    insumo = get_object_or_404(Insumo, id=id)
    return render(request, "insumos/detalle.html", {"insumo": insumo})
