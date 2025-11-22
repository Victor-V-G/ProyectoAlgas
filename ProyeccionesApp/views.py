from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from ProyectoAlgas.mongo import get_mongo_connection

def proyecciones_dashboard(request):
    return redirect("dashboard")  # o eliminar vista completa