from django.db import models


# ================================================================
# MODELO: RolModels
#
# Representa los roles del sistema y los permisos asociados a cada uno.
#
# Este modelo permite:
#   - Definir distintos tipos de roles (Admin, Gerente, Encargado, etc.)
#   - Asociar permisos específicos a cada rol.
#
# Los permisos se evalúan mediante decoradores (requiere_permiso)
# para restringir acceso a vistas o funcionalidades.
#
# Tabla física en la BD: "Rol"
# ================================================================
class RolModels(models.Model):

    # ------------------------------------------------------------
    # ID PRIMARIO DEL ROL
    #
    # AutoField:
    #   → Se incrementa automáticamente.
    #
    # verbose_name:
    #   → Nombre descriptivo para Django Admin.
    # ------------------------------------------------------------
    RolId = models.AutoField(
        primary_key=True,
        verbose_name='Rol Id'
    )

    # ------------------------------------------------------------
    # NOMBRE DEL ROL
    #
    # Ejemplos:
    #   - RolAdmin
    #   - Gerente
    #   - EncargadoStock
    #   - Operario
    #
    # db_column:
    #   → nombre del campo en la base de datos.
    # ------------------------------------------------------------
    NombreRol = models.CharField(
        max_length=20,
        db_column='NombreRol',
        verbose_name='Nombre del rol',
    )

    # ------------------------------------------------------------
    # DESCRIPCIÓN DEL ROL
    #
    # Describe el propósito o alcance del rol.
    # Ejemplo: "Administrador del sistema", "Operario de bodega".
    # ------------------------------------------------------------
    DescripcionRol = models.CharField(
        max_length=100,
        db_column='DescripcionRol',
        verbose_name='Descripcion del rol'
    )

    # ------------------------------------------------------------
    # PERMISOS DEL ROL
    #
    # Cada permiso es un BooleanField:
    #
    #   PermisoVerDashboard       → acceso al panel ejecutivo
    #   PermisoEditarStock        → permite crear/editar stock
    #   PermisoCrearContratos     → permite gestionar contratos
    #
    # Estos permisos se utilizan en decoradores como:
    #   @requiere_permiso("PermisoEditarStock")
    #
    # para controlar accesos a vistas.
    # ------------------------------------------------------------

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

    # ------------------------------------------------------------
    # METADATOS DEL MODELO
    #
    # db_table:
    #   → Nombre exacto de la tabla en la base de datos.
    # ------------------------------------------------------------
    class Meta:
        db_table = 'Rol'

    # ------------------------------------------------------------
    # REPRESENTACIÓN EN TEXTO
    #
    # Facilita visualizar el rol en admin, auditorías y logs.
    # ------------------------------------------------------------
    def __str__(self):
        return f"{self.NombreRol}"
