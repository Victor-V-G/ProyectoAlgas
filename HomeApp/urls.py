from django.urls import path, include
from . import views

# ===============================================================
# HomeApp/urls.py
#
# Archivo de enrutamiento principal del Dashboard Ejecutivo.
#
# Este módulo:
#   - Define la ruta principal del dashboard
#   - Incluye las rutas de todos los submódulos del sistema:
#       * StockApp
#       * ContratoApp
#       * EspecieApp
#       * InsumoApp
#       * AuditoriaApp
#       * ProyeccionesApp
#
# Funciona como el "hub" central del sistema, agrupando módulos.
# ===============================================================
urlpatterns = [

    # -----------------------------------------------------------
    # DASHBOARD EJECUTIVO
    #
    # URL:
    #     /
    #
    # Vista:
    #     dashboard_ejecutivo
    #
    # Name:
    #     "dashboard"
    #
    # Esta vista muestra el panel general con KPIs, gráficos,
    # proyecciones, inventario y alertas.
    # -----------------------------------------------------------
    path('', views.dashboard_ejecutivo, name="dashboard"),

    # -----------------------------------------------------------
    # MÓDULO: STOCK
    #
    # URL BASE:
    #     /stock/
    #
    # Incluye:
    #     StockApp/urls.py
    #
    # Funciones:
    #     - CRUD de Maxisacos
    #     - Detalles de stock
    #     - Auditoría de movimientos
    # -----------------------------------------------------------
    path("stock/", include("StockApp.urls")),

    # -----------------------------------------------------------
    # MÓDULO: CONTRATOS
    #
    # URL BASE:
    #     /contratos/
    #
    # Incluye:
    #     ContratoApp/urls.py
    #
    # Funciones:
    #     - Gestión de contratos
    #     - Entregas contractuales
    #     - Integración con dashboard
    # -----------------------------------------------------------
    path("contratos/", include("ContratoApp.urls")),

    # -----------------------------------------------------------
    # MÓDULO: ESPECIES DE ALGAS
    #
    # URL BASE:
    #     /especies/
    #
    # Incluye:
    #     EspecieApp/urls.py
    #
    # Funciones:
    #     - CRUD de especies
    #     - Listados
    #     - Detalles
    # -----------------------------------------------------------
    path("especies/", include("EspecieApp.urls")),

    # -----------------------------------------------------------
    # MÓDULO: INSUMOS
    #
    # URL BASE:
    #     /insumos/
    #
    # Incluye:
    #     InsumoApp/urls.py
    #
    # Funciones:
    #     - CRUD de insumos
    #     - Gestión de stock operativo
    #     - Auditoría
    # -----------------------------------------------------------
    path("insumos/", include("InsumoApp.urls")),

    # -----------------------------------------------------------
    # MÓDULO: AUDITORÍA
    #
    # URL BASE:
    #     /auditoria/
    #
    # Incluye:
    #     AuditoriaApp/urls.py
    #
    # Funciones:
    #     - Registro de acciones del sistema
    #     - Seguimiento de usuarios
    #     - Visualización de historial
    # -----------------------------------------------------------
    path("auditoria/", include("AuditoriaApp.urls")),

    # -----------------------------------------------------------
    # MÓDULO: PROYECCIONES
    #
    # URL BASE:
    #     /proyecciones/
    #
    # Incluye:
    #     ProyeccionesApp/urls.py
    #
    # Funciones:
    #     - Actualización de proyecciones (microservicio)
    #     - Carga de proyecciones desde MongoDB
    # -----------------------------------------------------------
    path("proyecciones/", include("ProyeccionesApp.urls")),
]
