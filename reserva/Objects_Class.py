from Resource import Resource
from datetime import datetime
class Car(Resource):
    def __init__(self,car,hours_available,type='Carro',approver=None,email=None,requester=None,reason=None,date=None,hour=None,status=None):
        super().__init__(type, approver, email, requester, reason, date, hour, status)
        self.car=car
        self.hours_available=hours_available.split(',')[1:]#index 0 is empty


    # carro=models.CharField(max_length=100)
    # aprovador=models.CharField(max_length=100, default='Antônio Rezende')
    # email=models.EmailField(max_length=254, default='antoniorezende@sicoob.com.br')
    # solicitante=models.CharField(max_length=100,null=True,blank=True)
    # motivo=models.CharField(max_length=100,null=True,blank=True)
    # email_solicitante=models.EmailField(max_length=254,null=True,blank=True)
    # data = models.DateField(null=True, blank=True)
    # hora = models.CharField(max_length=11,null=True, blank=True)
    # aprovado = models.BooleanField(null=True, blank=True)
    # created_at=models.DateField(auto_now_add=True)