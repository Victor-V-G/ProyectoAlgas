from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from UsuariosApp.models import UsuariosModels # tu modelo real de usuario
from .models import Maxisaco
from .forms import MaxisacoForm


def get_user_from_session(request):
    """
    Recupera el usuario según tu sistema de sesiones propio.
    """
    username = request.session.get("Usuario_Ingresado")

    if not username:
        return None

    try:
        return UsuariosModels.objects.get(Username=username)
    except UsuariosModels.DoesNotExist:
        return None


def stock_list(request):
    maxisacos = Maxisaco.objects.all().order_by("-fecha_registro")
    return render(request, "stock/lista.html", {"maxisacos": maxisacos})


def stock_crear(request):
    usuario = get_user_from_session(request)

    if request.method == "POST":
        form = MaxisacoForm(request.POST)
        if form.is_valid():
            m = form.save(commit=False)

            m.registrado_por = usuario
            m.actualizado_por = usuario

            m.save()
            messages.success(request, "Registro de stock agregado.")
            return redirect("stock")
    else:
        form = MaxisacoForm()

    return render(request, "stock/crear.html", {"form": form})


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


def stock_eliminar(request, id):
    m = get_object_or_404(Maxisaco, id=id)
    m.delete()
    messages.success(request, "Registro eliminado.")
    return redirect("stock")


def stock_detalle(request, id):
    m = get_object_or_404(Maxisaco, id=id)
    return render(request, "stock/detalle.html", {"m": m})
