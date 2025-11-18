from django.db import models

# Create your models here.
class RolModels(models.Model):

    RolId = models.AutoField(
        primary_key=True,
        verbose_name='Rol Id'
    )


    NombreRol = models.CharField(
        max_length=20,
        db_column='NombreRol',
        verbose_name='Nombre del rol',
    )


    DescripcionRol = models.CharField(
        max_length=100,
        db_column='DescripcionRol',
        verbose_name='Descripcion del rol'
    )


    PermisoVerDashboard = models.BooleanField(
        db_column='PermisoVerDashboard',
        verbose_name='Permiso de ver dashboard'
    )


    PermisoEditarStock = models.BooleanField(
        db_column='PermisoEditarStock',
        verbose_name='Permiso de editar stock'
    )


    PermisoCrearContratos = models.BooleanField(
        db_column='PermisoCrearContratos',
        verbose_name='Permiso de crear contratos'
    )


    class Meta:
        db_table = 'Rol'
        