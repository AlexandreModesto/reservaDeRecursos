from django.db import models

# Create your models here.

class Resources(models.Model):
    type=models.CharField(max_length=10)
    name=models.CharField(max_length=50,null=False,blank=False)
    approver = models.CharField(max_length=100,null=False,blank=False)
    email = models.EmailField(max_length=100,null=False,blank=False)
    hours_registred =models.JSONField(null=True)#hours / reasons / status

    def register_Hours(self,list_of_hours):
        dict_aux={}
        for hours in list_of_hours:
            dict_aux[hours]={}
        self.hours_registred=dict_aux
    def __str__(self):
        return self.name



class Carro(models.Model):
    carro=models.ForeignKey(Resources,on_delete=models.DO_NOTHING,default='')
    solicitante=models.CharField(max_length=100,null=True,blank=True)
    motivo=models.CharField(max_length=100,null=True,blank=True)
    email_solicitante=models.EmailField(max_length=254,null=True,blank=True)
    data = models.DateField(null=True, blank=True)
    hora = models.JSONField(null=False)
    aprovado = models.BooleanField(null=True, blank=True)
    created_at=models.DateField(auto_now_add=True)

    class Meta:
        abstract = False

    def __str__(self):
        return self.carro.name
class Sala(models.Model):
    sala=models.CharField(max_length=100)
    aprovador=models.CharField(max_length=100)
    email=models.EmailField(max_length=254)
    solicitante = models.CharField(max_length=100, null=True,blank=True)
    motivo = models.CharField(max_length=100, null=True, blank=True)
    email_solicitante = models.EmailField(max_length=254, null=True,blank=True)
    data = models.DateField(null=True, blank=True)
    hora=models.CharField(max_length=11,null=True,blank=True)
    aprovado=models.BooleanField(null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = False

    def __str__(self):
        return self.sala