
from django.urls import path
from .views import RenderHome

urlpatterns = [

    path('home/', RenderHome, name='Home'),

]