from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard_ejecutivo, name="dashboard"),

    path("stock/", include("StockApp.urls")),

    path("contratos/", include("ContratoApp.urls")),

    path("especies/", include("EspecieApp.urls")),

    path("insumos/", include("InsumoApp.urls")),

]
