from django.urls import path
from .views import VerVista

urlpatterns = [
    path('', VerVista)
]