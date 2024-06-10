from django.contrib import admin

from .models import Carro,Sala, Resources


class ListandoCarros(admin.ModelAdmin):
    list_display = ("id","carro","solicitante","email_solicitante","aprovado","created_at")
    list_display_links = ("id", "carro")

class ListandoSalas(admin.ModelAdmin):
    list_display = ('id','sala',"data","solicitante","email_solicitante","aprovado","created_at")
    list_display_links = ("id", "sala")

class ListandoRecursos(admin.ModelAdmin):
    list_display = ('id','type','name')
    list_display_links = ("id",'name')

admin.site.register(Carro, ListandoCarros)
admin.site.register(Sala, ListandoSalas)
admin.site.register(Resources,ListandoRecursos)


