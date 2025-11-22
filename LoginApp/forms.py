from django import forms

class LoginForm(forms.Form):
    
    UsernameField = forms.CharField(
        label='Nombre de usuario'
    )

    PasswordField = forms.CharField(
        label='Contraseña'
    )

    class Meta:
        fields = ['UsernameField', 'PasswordField']