from django.shortcuts import render

# Create your views here.
def RenderHome(request):
    return render(request, 'Home/Home.html')
