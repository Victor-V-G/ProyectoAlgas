from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.hashers import make_password


# ============================================================
# Función que se ejecutará después de cada migrate del proyecto
# Su propósito es:
#   1. Crear roles por defecto (si no existen)
#   2. Crear usuarios por defecto (si no existen)
# Esta técnica es útil para cargar "datos iniciales" sin fixtures.
# ============================================================
def AutoAddDefaults(sender, **kwargs):

    # ------------------------------------------------------------
    # Import interno de los modelos para evitar errores de carga
    # como "AppRegistryNotReady" cuando Django inicializa las apps.
    # ------------------------------------------------------------
    from RolApp.models import RolModels
    from UsuariosApp.models import UsuariosModels

    # ============================================================
    # 1. LISTA DE ROLES QUE DEBEN EXISTIR EN EL SISTEMA
    # Se definen como diccionarios para facilitar su creación.
    # ============================================================
    roles_definidos = [
        {
            "NombreRol": "RolAdmin",
            "DescripcionRol": "Administrador del sistema",
            "PermisoVerDashboard": True,
            "PermisoEditarStock": True,
            "PermisoCrearContratos": True,
        },
        {
            "NombreRol": "Gerente",
            "DescripcionRol": "Gerente Comercial",
            "PermisoVerDashboard": True,
            "PermisoEditarStock": False,
            "PermisoCrearContratos": True,
        },
        {
            "NombreRol": "EncargadoStock",
            "DescripcionRol": "Responsable del inventario",
            "PermisoVerDashboard": False,
            "PermisoEditarStock": True,
            "PermisoCrearContratos": False,
        },
        {
            "NombreRol": "Operario",
            "DescripcionRol": "Operario de apoyo",
            "PermisoVerDashboard": False,
            "PermisoEditarStock": True,
            "PermisoCrearContratos": True,
        },
    ]

    # Diccionario donde se guardarán los roles reales creados/buscados
    # para luego asignarlos a los usuarios por defecto.
    roles_creados = {}

    # ============================================================
    # CREACIÓN AUTOMÁTICA DE ROLES
    # get_or_create permite:
    #   - obtener rol existente
    #   - crear uno nuevo si no existe
    # ============================================================
    for rol in roles_definidos:
        obj, creado = RolModels.objects.get_or_create(
            NombreRol=rol["NombreRol"],       # Condición de búsqueda
            defaults={                         # Valores si se crea
                "DescripcionRol": rol["DescripcionRol"],
                "PermisoVerDashboard": rol["PermisoVerDashboard"],
                "PermisoEditarStock": rol["PermisoEditarStock"],
                "PermisoCrearContratos": rol["PermisoCrearContratos"],
            },
        )

        # Guardamos el objeto rol en el diccionario
        roles_creados[rol["NombreRol"]] = obj

        # Mensaje de consola informativo
        if creado:
            print(f"✔ Rol creado: {rol['NombreRol']}")
        else:
            print(f"ℹ Rol ya existente: {rol['NombreRol']}")

    # ============================================================
    # 2. USUARIOS QUE DEBEN EXISTIR POR DEFECTO EN EL SISTEMA
    # Contraseñas se encriptarán antes de guardarse.
    # ============================================================
    usuarios_defecto = [
        {
            "Username": "Admin",
            "Password": "Admin123",
            "Nombre": "Administrador",
            "Apellido": "Principal",
            "Email": "admin@sistema.com",
            "Rut": "00000000-0",
            "Telefono": "000000000",
            "Rol": "RolAdmin",
        },
        {
            "Username": "gerente",
            "Password": "Gerente123",
            "Nombre": "Gerente",
            "Apellido": "General",
            "Email": "gerente@sistema.com",
            "Rut": "11111111-1",
            "Telefono": "111111111",
            "Rol": "Gerente",
        },
        {
            "Username": "stock",
            "Password": "Stock123",
            "Nombre": "Encargado",
            "Apellido": "Bodega",
            "Email": "stock@sistema.com",
            "Rut": "22222222-2",
            "Telefono": "222222222",
            "Rol": "EncargadoStock",
        },
        {
            "Username": "operario",
            "Password": "Operario123",
            "Nombre": "Operario",
            "Apellido": "Planta",
            "Email": "operario@sistema.com",
            "Rut": "33333333-3",
            "Telefono": "333333333",
            "Rol": "Operario",
        },
    ]

    # ============================================================
    # CREACIÓN AUTOMÁTICA DE USUARIOS POR DEFECTO
    # - Se verifica existencia por Username
    # - La contraseña se guarda encriptada
    # - Se asigna el rol previamente creado
    # ============================================================
    for u in usuarios_defecto:

        # Verificar si el usuario ya existe para evitar duplicados
        if not UsuariosModels.objects.filter(Username=u["Username"]).exists():

            # Crear usuario nuevo con contraseña encriptada
            UsuariosModels.objects.create(
                Username=u["Username"],
                Password=make_password(u["Password"]),  # Encripta contraseña
                Email=u["Email"],
                Nombre=u["Nombre"],
                Apellido=u["Apellido"],
                Rut=u["Rut"],
                Telefono=u["Telefono"],
                EstadoUsuario=True,
                Rol=roles_creados[u["Rol"]],           # Asigna el rol correspondiente
            )

            print(f"✔ Usuario creado: {u['Username']}")

        else:
            print(f"ℹ Usuario ya existente: {u['Username']}")


# ============================================================
# CONFIGURACIÓN DE LA APLICACIÓN UsuariosApp
# Aquí se engancha la señal post_migrate
# ============================================================
class UsuariosappConfig(AppConfig):

    # Tipo de ID por defecto
    default_auto_field = 'django.db.models.BigAutoField'

    # Nombre de la app según Django
    name = 'UsuariosApp'

    # ------------------------------------------------------------
    # Método ready():
    # - Se ejecuta cuando la app está totalmente cargada
    # - Aquí conectamos la señal post_migrate
    # ------------------------------------------------------------
    def ready(self):
        # post_migrate → se dispara después de cada migrate
        # sender=self → solo ejecuta esta carga para esta app
        post_migrate.connect(AutoAddDefaults, sender=self)
