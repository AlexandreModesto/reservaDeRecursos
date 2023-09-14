from django.urls import path
from .views import index,carro,sala, login, aprovar_carro,aprovar_sala,reservas,reserva_mes,reservas_json

urlpatterns = [
    path('', index,name='index'),
    path('carros/<str:carro>/<str:result>',carro,name='carros'),
    path('salas',sala,name='salas'),
    path('login',login,name='login'),
    path('aprovarCarro',aprovar_carro,name='aprovarCarro'),
    path('aprovarSala',aprovar_sala,name='aprovarSala'),
    path('reservas/<str:item>',reservas,name='reservas'),
    path('reservas/<db>/<mes>',reserva_mes,name='reservaMes'),
    path('json/<str:item>',reservas_json,name='json')
]