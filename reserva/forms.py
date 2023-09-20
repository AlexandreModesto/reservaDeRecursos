#-*-coding:utf-8 -*-
from django import forms
import  datetime

class ReservaCarro(forms.Form):
    carroChoices=(('Ford Ka','Ford Ka'),('Onix','Onix'),('HB20','HB20'),)
    carro=forms.ChoiceField(choices=carroChoices,label='Qual carro?',required=False)
    nome = forms.CharField(label='Digite seu nome', max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome sobrenome', }))
    email = forms.EmailField(label='Digite seu email', max_length=100,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@email.com'}))
    motivo=forms.CharField(label='Qual o motivo?', max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Viagem para BOT'}))
    horas_choice=(('07:50-08:50','07:50 - 08:50'),('08:51-09:50','08:51 - 09:50'),('09:51-10:50','09:51 - 10:50'),
           ('10:51-11:50','10:51 - 11:50'),('11:51-12:50','11:51 - 12:50'),('12:51-13:50','12:51 - 13:50'),
           ('13:51-14:50','13:51 - 14:50'),('14:51-15:50','14:51 - 15:50'),('15:51-17:15','15:51 - 17:15'))
    horas=forms.ChoiceField(choices=horas_choice,label='Horário :',widget=forms.RadioSelect())
    repetir=forms.BooleanField(required=False,label='Repetir',)


class ReservaSala(forms.Form):
    salaChoices=(('Sala Terreo','Sala no Terreo'),('Sala andar 1','Sala do 1°andar'),('Sala Conad Maior','Sala Maior do Conad'),('Sala Conad Menor','Sala Menor do Conad'),('Auditório','Auditório'))
    salas=forms.ChoiceField(choices=salaChoices,label='Qual sala?')
    nome = forms.CharField(label='Digite seu nome', max_length=100,
                           widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nome sobrenome',}))
    email = forms.EmailField(label='Digite seu email', max_length=100,
                             widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'email@email.com'}))
    motivo = forms.CharField(label='Qual o motivo?', max_length=100,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reunião da Diretoria'}))
    horas_choice = (('07:50-08:30', '07:50 - 08:30'), ('08:31-09:00', '08:31 - 09:00'), ('09:01-09:30', '09:01 - 09:30'),
             ('09:31-10:00', '09:31 - 10:00'), ('10:01-10:30', '10:01 - 10:30'), ('10:31-11:00', '10:31 - 11:00'),
             ('11:31-12:00', '11:31 - 12:00'), ('12:01-12:30', '12:01 - 12:30'), ('12:31-13:00', '12:31 - 13:00'),
             ('13:01-13:30', '13:01 - 13:30'), ('13:31-14:00', '13:31 - 14:00'), ('14:01-14:30', '14:01 - 14:30'),
             ('14:31-15:00', '14:31 - 15:00'), ('15:01-15:30', '15:01 - 15:30'), ('15:31-16:00', '15:31 - 16:00'),
             ('16:01-16:30', '16:01 - 16:30'), ('16:31-17:15', '16:31 - 17:15'))
    horas = forms.ChoiceField(choices=horas_choice, label='Horário :', widget=forms.RadioSelect())
    auditorio_choice = (('08:00-12:00', '08:00 - 12:00'), ('12:01-17:00', '12:01 - 17:00'), ('17:01-22:50', '17:01 - 22:50'))
    auditorio = forms.ChoiceField(choices=auditorio_choice, label='Horário :', widget=forms.RadioSelect())
    repetir = forms.BooleanField(required=False, label='Repetir', )


# def return_options()
# class ReservaSala2(f)
class LoginForms(forms.Form):
    usuario=forms.CharField(label='Usuario', max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'similar a VPN',}))
    senha=forms.CharField(label='Senha', max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'senha',}))

def return_month(date,now=False,one=False,two=False):
    hoje=datetime.datetime.now()
    dict={1:'Janeiro',2:'Fevereiro',3:'Março',4:'Abril',5:'Maio',6:'Junho',7:'Julho',8:'Agosto',9:'Setembro',10:'Outubro',11:'Novembro',12:'Dezembro'}
    if not now == False:
        return dict[hoje.month]
    elif not one == False:
        return dict[hoje.month+1]
    else:
        return dict[hoje.month+2]
class ReservasForm(forms.Form):
    date=datetime.datetime.now()
    meses=((return_month(date,now=True),(return_month(date,now=True))),(return_month(date,one=True),return_month(date,one=True)),(return_month(date,two=True),return_month(date,two=True)))
    mes=forms.ChoiceField(choices=meses,label='Qual Mês? ')