from django.shortcuts import render

# Create your views here.
def VerVista(request):
    return render(request, 'prueba/hola.html')