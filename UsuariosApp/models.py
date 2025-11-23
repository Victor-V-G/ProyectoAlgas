from django.db import models
from django.db.models.constraints import UniqueConstraint
from RolApp.models import RolModels

# Modelo principal de usuarios del sistema
class UsuariosModels(models.Model):

    # --------------------------------------------
    # Identificador primario del usuario
    # --------------------------------------------
    UsuarioID = models.AutoField(
        primary_key=True,
        verbose_name='Id del usuario',
    )

    # --------------------------------------------
    # Nombre de usuario (para login)
    # - Debe ser único
    # - 30 caracteres máx.
    # --------------------------------------------
    Username = models.CharField(
        max_length=30,
        db_column='Username',
        error_messages={'unique': 'Intente con otro nombre de usuario'}
    )

    # --------------------------------------------
    # Contraseña del usuario
    # - Se almacena encriptada (hash)
    # - Campo largo para hashes seguros
    # --------------------------------------------
    Password = models.CharField(
        max_length=200,
        db_column='Password',
    )

    # --------------------------------------------
    # Email del usuario
    # - Único en el sistema
    # - Valida formato email automáticamente
    # --------------------------------------------
    Email = models.EmailField(
        db_column='Email',
        error_messages={'unique': 'Este email ya esta siendo ocupado'}
    )

    # --------------------------------------------
    # Nombre real del usuario
    # --------------------------------------------
    Nombre = models.CharField(
        max_length=30,
        db_column='Nombre',
    )

    # --------------------------------------------
    # Apellido del usuario
    # --------------------------------------------
    Apellido = models.CharField(
        max_length=40,
        db_column='Apellido'
    )

    # --------------------------------------------
    # RUT chileno del usuario
    # - Único en el sistema
    # - Validado externamente en formularios
    # --------------------------------------------
    Rut = models.CharField(
        max_length=10,
        db_column='Rut',
        error_messages={'unique': 'Este rut ya esta siendo ocupado'}
    )

    # --------------------------------------------
    # Teléfono del usuario
    # --------------------------------------------
    Telefono = models.CharField(
        max_length=20,
        db_column='Telefono'
    )

    # --------------------------------------------
    # Estado del usuario
    # Puede ser:
    # - True: Activo
    # - False: Desactivado (no puede acceder)
    # --------------------------------------------
    EstadoUsuario = models.BooleanField(
        db_column='EstadoUsuario',
        verbose_name='Estado del usuario'
    )

    # --------------------------------------------
    # Fecha de creación del registro
    # Se genera automáticamente al crear un usuario
    # --------------------------------------------
    FechaCreacion = models.DateTimeField(
        auto_now_add=True,
        db_column='FechaCreacion',
        verbose_name='Fecha de creacion'
    )

    # --------------------------------------------
    # Relación con el modelo de Rol
    # - Un usuario puede tener solo un rol
    # - Si se elimina un Rol, el usuario queda con Rol NULL
    # --------------------------------------------
    Rol = models.ForeignKey(
        RolModels,
        blank=True,
        null=True,
        related_name='Usuario',
        db_column='RolId',
        on_delete=models.SET_NULL
    )

    # --------------------------------------------
    # Configuración de la tabla y restricciones
    # --------------------------------------------
    class Meta:
        db_table = 'Usuarios'

        # UniqueConstraints:
        # Garantizan que no existan duplicados en los campos críticos
        constraints = [
            UniqueConstraint(fields=['Username'], name='unique_username'),
            UniqueConstraint(fields=['Email'], name='unique_email'),
            UniqueConstraint(fields=['Rut'], name='unique_rut'),
        ]
