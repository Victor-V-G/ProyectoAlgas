from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.hashers import make_password


def AutoAddDefaults(sender, **kwargs):
    from RolApp.models import RolModels
    from UsuariosApp.models import UsuariosModels

    # ============================================================
    # 1. ROLES A CREAR
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

    roles_creados = {}

    # CREAR ROLES
    for rol in roles_definidos:
        obj, creado = RolModels.objects.get_or_create(
            NombreRol=rol["NombreRol"],
            defaults={
                "DescripcionRol": rol["DescripcionRol"],
                "PermisoVerDashboard": rol["PermisoVerDashboard"],
                "PermisoEditarStock": rol["PermisoEditarStock"],
                "PermisoCrearContratos": rol["PermisoCrearContratos"],
            },
        )
        roles_creados[rol["NombreRol"]] = obj
        if creado:
            print(f"✔ Rol creado: {rol['NombreRol']}")
        else:
            print(f"ℹ Rol ya existente: {rol['NombreRol']}")

    # ============================================================
    # 2. USUARIOS POR DEFECTO
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

    # CREAR USUARIOS
    for u in usuarios_defecto:
        if not UsuariosModels.objects.filter(Username=u["Username"]).exists():
            UsuariosModels.objects.create(
                Username=u["Username"],
                Password=make_password(u["Password"]),
                Email=u["Email"],
                Nombre=u["Nombre"],
                Apellido=u["Apellido"],
                Rut=u["Rut"],
                Telefono=u["Telefono"],
                EstadoUsuario=True,
                Rol=roles_creados[u["Rol"]],
            )
            print(f"✔ Usuario creado: {u['Username']}")
        else:
            print(f"ℹ Usuario ya existente: {u['Username']}")


class UsuariosappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'UsuariosApp'

    def ready(self):
        post_migrate.connect(AutoAddDefaults, sender=self)
