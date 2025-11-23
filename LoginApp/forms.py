from django import forms


# ===============================================================
# FORMULARIO: LoginForm
#
# Este formulario se utiliza en la vista RenderLoginForm para:
#   - Mostrar campos de credenciales al usuario
#   - Validar que los campos no estén vacíos
#
# Nota:
#   La autenticación REAL (verificar existencia del usuario y
#   validar la contraseña) se realiza en la vista usando el
#   modelo UsuariosModels y la función check_password.
#
# Este formulario solo valida requisitos mínimos del frontend.
# ===============================================================
class LoginForm(forms.Form):

    # -----------------------------------------------------------
    # UsernameField:
    #   - Campo de texto para ingresar el nombre de usuario.
    #   - Django validará automáticamente que no esté vacío.
    #   - error_messages permite personalizar los mensajes.
    # -----------------------------------------------------------
    UsernameField = forms.CharField(
        label='Nombre de usuario',
        error_messages={
            'required': 'Este campo no puede quedar vacío.'
        }
    )

    # -----------------------------------------------------------
    # PasswordField:
    #   - Campo tipo contraseña (input type="password").
    #   - Se utiliza PasswordInput para ocultar los caracteres.
    #   - Django valida que no esté vacío.
    # -----------------------------------------------------------
    PasswordField = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Este campo no puede quedar vacío.'
        }
    )

    # -----------------------------------------------------------
    # Meta:
    #   Define qué campos forman parte del formulario.
    #   Aunque forms.Form no requiere Meta obligatoriamente,
    #   se incluye para mantener claridad y organización.
    # -----------------------------------------------------------
    class Meta:
        fields = ['UsernameField', 'PasswordField']
