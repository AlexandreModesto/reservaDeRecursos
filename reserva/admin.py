from django.contrib import admin

from .models import Carro,Sala


class ListandoCarros(admin.ModelAdmin):
    list_display = ("id", "carro","dataInit","solicitante","aprovado")

class ListandoSalas(admin.ModelAdmin):
    list_display = ('id','sala',"dataInit","solicitante","aprovado")

admin.site.register(Carro, ListandoCarros)
admin.site.register(Sala, ListandoSalas)


