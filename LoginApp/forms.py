from django import forms

class LoginForm(forms.Form):

    UsernameField = forms.CharField(
        label='Nombre de usuario',
        error_messages={
            'required': 'Este campo no puede quedar vacío.'
        }
    )

    PasswordField = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput, 
        error_messages={
            'required': 'Este campo no puede quedar vacío.'
        }
    )

    class Meta:
        fields = ['UsernameField', 'PasswordField']
