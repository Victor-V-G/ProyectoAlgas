from django.urls import path
from .views import RenderLoginForm, RenderLogout

urlpatterns = [

    path('', RenderLoginForm, name='Login'),

    path('logout/', RenderLogout, name='logout')

]