from .Resource import Resource
from datetime import datetime
class Carro_Class(Resource):
    def __init__(self,car,hours_available,type='Carro',approver=None,email=None,requester=None,reason=None,date=None,hour=None,status=None):
        super().__init__(type, approver, email, requester, reason, date, hour, status)
        self.car=car
        self.hours_available=hours_available


    def getHours_available(self):
        return self.hours_available

    def extract_hour(self,hour):
        return datetime.strptime(hour.split()[0], '%H:%M')

    def manipulte_hours(self,update=None):#index 0 is empty
        if update == None:
            hours=self.hours_available.split(',')[1:]
        else:
            hours=update
        for h in hours:
            hour1=h.split(' até ')[0]
            hour2 = h.split(' até ')[1]
            hour1_f=datetime.strptime(hour1,'%H:%M')
            hour2_f = datetime.strptime(hour2, '%H:%M')
            if hour1_f >= hour2_f:
                return print("Hora inicial deve ser maior que hora final")

        self.hours_available=sorted(hours,key=self.extract_hour)
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