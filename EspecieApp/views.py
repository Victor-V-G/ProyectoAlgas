from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Especie
from .forms import EspecieForm

def especies_list(request):
    especies = Especie.objects.all().order_by("nombre")
    return render(request, "especies/lista.html", {"especies": especies})


def especie_crear(request):
    if request.method == "POST":
        form = EspecieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Especie creada.")
            return redirect("especies_list")
    else:
        form = EspecieForm()

    return render(request, "especies/crear.html", {"form": form})



def especie_editar(request, id):
    especie = get_object_or_404(Especie, id=id)

    if request.method == "POST":
        form = EspecieForm(request.POST, instance=especie)
        if form.is_valid():
            form.save()
            messages.success(request, "Especie actualizada.")
            return redirect("especies_list")
    else:
        form = EspecieForm(instance=especie)

    return render(request, "especies/editar.html", {
        "form": form,
        "especie": especie
    })



def especie_eliminar(request, id):
    especie = get_object_or_404(Especie, id=id)
    especie.delete()
    messages.success(request, "Especie eliminada.")
    return redirect("especies_list")



def especie_detalle(request, id):
    especie = get_object_or_404(Especie, id=id)
    return render(request, "especies/detalle.html", {"especie": especie})

