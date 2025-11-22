from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Auditoria

def auditoria_list(request):
    auditorias = Auditoria.objects.all().order_by("-fecha")
    return render(request, "auditoria/lista.html", {"auditorias": auditorias})


def auditoria_detalle(request, id):
    a = get_object_or_404(Auditoria, id=id)
    return render(request, "auditoria/detalle.html", {"a": a})
