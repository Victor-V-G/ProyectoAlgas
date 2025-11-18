from django.db import models
from django.db.models.constraints import UniqueConstraint
from RolApp.models import RolModels

# Create your models here.
class UsuariosModels(models.Model):

    UsuarioID = models.AutoField(
        primary_key=True,
        verbose_name='Id del usuario',
    )


    Username = models.CharField(
        max_length=30,
        db_column='Username',
        error_messages={'unique': 'Intente con otro nombre de usuario'}
    )


    Password = models.CharField(
        max_length=200,
        db_column='Password',
    )


    Email = models.EmailField(
        db_column='Email',
        error_messages={'unique': 'Este email ya esta siendo ocupado'}
    )


    Nombre = models.CharField(
        max_length=30,
        db_column='Nombre',
    )


    Apellido = models.CharField(
        max_length=40,
        db_column='Apellido'
    )


    Rut = models.CharField(
        max_length=10,
        db_column='Rut',
        error_messages={'unique': 'Este rut ya esta siendo ocupado'}
    )


    Telefono = models.CharField(
        max_length=20,
        db_column='Telefono'
    )


    EstadoUsuario = models.BooleanField(
        db_column='EstadoUsuario',
        verbose_name='Estado del usuario'
    )


    FechaCreacion = models.DateTimeField(
        auto_now_add=True,
        db_column='FechaCreacion',
        verbose_name='Fecha de creacion'
    )


    Rol = models.ForeignKey(
        RolModels,
        blank=True,
        null=True,
        related_name='Usuario',
        db_column='RolId',
        on_delete=models.SET_NULL
    )

    #Auditorias FK


    class Meta:
        db_table = 'Usuarios'
        constraints = [
            UniqueConstraint(fields=['Username'], name='unique_username'),
            UniqueConstraint(fields=['Email'], name='unique_email'),
            UniqueConstraint(fields=['Rut'], name='unique_rut'),
        ]
