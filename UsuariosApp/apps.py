from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.hashers import make_password

def AutoAddUser(sender, **kwargs):
    from .models import UsuariosModels
    from RolApp.models import RolModels
        
    if not UsuariosModels.objects.filter(Username="Admin"):

        Rol_id = RolModels.objects.filter(NombreRol="RolAdmin").first()
    
        UsuariosModels.objects.create(
            Username='Admin',
            Password=make_password('Admin123'),
            Email='POR DEFINIR',
            Nombre='POR DEFINIR',
            Apellido='POR DEFINIR',
            Rut='00000000-0',
            Telefono='000000000',
            EstadoUsuario=True,
            Rol=Rol_id,
        )

        print("Usuario administrador creado")


class UsuariosappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'UsuariosApp'

    def ready(self):
        post_migrate.connect(AutoAddUser, sender=self)