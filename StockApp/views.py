from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Maxisaco
from .forms import MaxisacoForm

def stock_list(request):
    maxisacos = Maxisaco.objects.all().order_by("-fecha_registro")
    return render(request, "stock/lista.html", {"maxisacos": maxisacos})


def stock_crear(request):
    if request.method == "POST":
        form = MaxisacoForm(request.POST)
        if form.is_valid():
            m = form.save(commit=False)
            m.registrado_por = request.user
            m.actualizado_por = request.user
            m.save()
            messages.success(request, "Registro de stock agregado.")
            return redirect("stock_list")
    else:
        form = MaxisacoForm()

    return render(request, "stock/crear.html", {"form": form})


def stock_editar(request, id):
    m = get_object_or_404(Maxisaco, id=id)

    if request.method == "POST":
        form = MaxisacoForm(request.POST, instance=m)
        if form.is_valid():
            maxisaco = form.save(commit=False)
            maxisaco.actualizado_por = request.user
            maxisaco.save()
            messages.success(request, "Registro actualizado.")
            return redirect("stock_list")
    else:
        form = MaxisacoForm(instance=m)

    return render(request, "stock/editar.html", {"form": form, "maxisaco": m})


def stock_eliminar(request, id):
    m = get_object_or_404(Maxisaco, id=id)
    m.delete()
    messages.success(request, "Registro eliminado.")
    return redirect("stock_list")


def stock_detalle(request, id):
    m = get_object_or_404(Maxisaco, id=id)
    return render(request, "stock/detalle.html", {"m": m})

