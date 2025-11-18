from django.apps import AppConfig
from django.db.models.signals import post_migrate

def AutoAddRol(sender, **kwargs):
    from .models import RolModels
    
    if not RolModels.objects.filter(NombreRol='RolAdmin'):
        RolModels.objects.create(
            NombreRol='RolAdmin',
            DescripcionRol='Rol unico de administrador',
            PermisoVerDashboard=True,
            PermisoEditarStock=True,
            PermisoCrearContratos=True
        )

    print("Rol unico de administrador creado")

class RolappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'RolApp'

    def ready(self):
        post_migrate.connect(AutoAddRol, sender=self)
