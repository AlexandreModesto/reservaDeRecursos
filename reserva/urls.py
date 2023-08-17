from django.urls import path
from .views import index,carro,sala, login, aprovar_carro,aprovar_sala

urlpatterns = [
    path('', index,name='index'),
    path('carros',carro,name='carros'),
    path('salas',sala,name='salas'),
    path('login',login,name='login'),
    path('aprovarCarro',aprovar_carro,name='aprovarCarro'),
    path('aprovarSala',aprovar_sala,name='aprovarSala'),
]