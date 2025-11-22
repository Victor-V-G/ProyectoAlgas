from django.urls import path
from .views import RenderLoginForm

urlpatterns = [

    path('', RenderLoginForm, name='Login'),

]