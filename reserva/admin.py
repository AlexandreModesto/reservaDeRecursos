from django.contrib import admin

from .models import Carro,Sala


class ListandoCarros(admin.ModelAdmin):
    list_display = ("id", "carro","data","solicitante","aprovado","created_at")
    list_display_links = ("id", "carro")

class ListandoSalas(admin.ModelAdmin):
    list_display = ('id','sala',"data","solicitante","aprovado","created_at")
    list_display_links = ("id", "sala")

admin.site.register(Carro, ListandoCarros)
admin.site.register(Sala, ListandoSalas)


