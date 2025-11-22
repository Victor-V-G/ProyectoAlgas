from django.shortcuts import render, redirect
from . import forms
from UsuariosApp.models import UsuariosModels
from django.contrib import messages
from django.contrib.auth.hashers import check_password
# Create your views here.


def RenderLoginForm(request):
    form = forms.LoginForm(request.POST)
    data = {'form': form}

    if request.method == "POST":
        UsernameField = request.POST['UsernameField']
        PasswordField = request.POST['PasswordField']

        if not UsuariosModels.objects.filter(Username=UsernameField):
            messages.error(request, "Contraseña o identificador de usuario incorrectos. Escriba la contraseña y el identificador de usuario correctos e inténtelo de nuevo.")
            return render(request, 'LoginTemplate/Form.html', data)
        else:
            UsuarioRecuperado = UsuariosModels.objects.get(Username=UsernameField)
            if check_password(PasswordField, UsuarioRecuperado.Password):
                request.session['Usuario_Ingresado'] = UsuarioRecuperado.Username

                UsuarioLogeado = request.session.get('Usuario_Ingresado')
                
                if UsuarioLogeado == 'Admin':
                    return redirect('Home')
                else:
                    pass

            else:
                messages.error(request, "Contraseña o identificador de usuario incorrectos. Escriba la contraseña y el identificador de usuario correctos e inténtelo de nuevo.")

    return render(request, 'LoginTemplate/Form.html', data)


def Logout(request):
    request.session.flush()
    return redirect('Login')