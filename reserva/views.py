#-*-coding:utf-8 -*-
import django.contrib.auth
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .models import Carro,Sala
from .forms import ReservaSala,ReservaCarro,LoginForms
from django.core.mail import EmailMessage
from django.contrib import messages
from datetime import date


def index(request):
    return render(request,'reserva/index.html')

def carro(request):
    carroForm = ReservaCarro()
    carroObjsTrue = Carro.objects.filter(aprovado=True,dataInit__gte=date.today()).values()
    carroObjsNone=Carro.objects.filter(aprovado=None,dataInit__gte=date.today()).values()
    modelComb= carroObjsNone | carroObjsTrue
    model= modelComb.order_by('-dataInit')
    if request.method == 'POST':
        carroForm = ReservaCarro(request.POST)
        if carroForm.is_valid():
            carro=carroForm.cleaned_data['carro']
            dataInit=request.POST.get('dataInit',None)
            dataEnd = request.POST.get('dataEnd', None)
            nome=carroForm.cleaned_data['nome']
            email=carroForm.cleaned_data['email']
            horaInit=request.POST.get('stt-time',None)
            horaEnd = request.POST.get('end-time', None)
            r=Carro(carro=carro,solicitante=nome,email_solicitante=email,dataInit=dataInit,dataEnd=dataEnd,horaEnd=horaEnd,horaInit=horaInit)
            r.save()
            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Nova Solicitação de Reserva</h1>
                                        <p><strong>{nome} esta solicitando reserva de carro pro dia <strong>{dataInit}</strong> até <strong>{dataEnd}</strong> horário: <strong>{horaInit}</strong> até <strong>{horaEnd}</strong></p>
                                        <p>Para aprovar ou não clique <a href='10.110.209.15/aprovarSala'>aqui</a></p>""",
                None,
                ['antoniorezende@sicoob.com.br'])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request,'Reserva encaminhada para Aprovação')
            return redirect('index')
    return render(request,'reserva/carro.html',{'carroForm':carroForm,'model':model})

def sala(request):
    salaForm = ReservaSala()
    salaObjsTrue = Sala.objects.filter(aprovado=True, dataInit__gte=date.today()).values()
    salaObjsNone = Sala.objects.filter(aprovado=None, dataInit__gte=date.today()).values()
    modelComb = salaObjsNone | salaObjsTrue
    model = modelComb.order_by('-dataInit')
    if request.method == 'POST':
        salaForm = ReservaSala(request.POST)
        if salaForm.is_valid():
            sala=salaForm.cleaned_data['salas']
            dataInit=request.POST.get('dataInit',None)
            dataEnd = request.POST.get('dataEnd', None)
            nome=salaForm.cleaned_data['nome']
            email=salaForm.cleaned_data['email']
            horaInit = request.POST.get('stt-time', None)
            horaEnd = request.POST.get('end-time', None)
            if sala=='Sala Conad Menor' or sala=='Sala Conad Maior':
                apro='Maria Valdirene'
                mail='valdirene.monteiro@sicoob.com.br'
            else:
                apro = 'Mayara Alvarenga'
                mail = 'mayara.alvarenga@sicoob.com.br'
            s=Sala(sala=sala,aprovador=apro,email=mail,solicitante=nome,email_solicitante=email,dataInit=dataInit,dataEnd=dataEnd,horaEnd=horaEnd,horaInit=horaInit)
            s.save()
            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Nova Solicitação de Reserva</h1>
                            <p><strong>{nome} esta solicitando reserva da {sala} pro dia <strong>{dataInit}</strong> até <strong>{dataEnd}</strong> horário: <strong>{horaInit}</strong> até <strong>{horaEnd}</strong></p>
                            <p>Para aprovar ou não clique <a href='10.110.209.15/aprovarSala'>aqui</a></p>""",
                None,
                [mail])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request, 'Reserva encaminhada para Aprovação')
            return redirect('index')
    return render(request,'reserva/sala.html',{'salaForm':salaForm,'model':model})

def login(request):
    login = LoginForms()
    if request.method=='POST':
        loginForm = LoginForms(request.POST)
        if loginForm.is_valid():
            usuario=loginForm.cleaned_data['usuario']
            senha = loginForm.cleaned_data['senha']
            user = authenticate(request,username=usuario,password=senha)
            if user is not None:
                django.contrib.auth.login(request,user)
                messages.success(request,'Usuário Logado')
                if not usuario == 'rezendea':
                    return redirect('aprovarSala')
                else:
                    return redirect('aprovarCarro')
            else:
                messages.error(request, 'Acesso Negado')
                return redirect('login')
    return render(request,'reserva/login.html',{'login':login})

def aprovar_carro(request):
    if not request.user.username.endswith('rezendea'):
        return redirect('login')
    retorna_soli = Carro.objects.filter(aprovado=None)
    carroObjsTrue = Carro.objects.filter(aprovado=True, dataInit__gte=date.today()).values()
    carroObjsNone = Carro.objects.filter(aprovado=None, dataInit__gte=date.today()).values()
    modelComb = carroObjsNone | carroObjsTrue
    model = modelComb.order_by('-dataInit')
    if request.method =="POST":
        check = request.POST.get('botao')
        id = request.POST.get('id')
        obj = Carro.objects.filter(id=id).values('carro','dataInit','dataEnd','horaInit','horaEnd','email_solicitante')
        valores=[]
        for campo,valor in obj[0].items():
            valores.append(valor)

        if check == 'aprovar':
            Carro.objects.filter(id=id).update(aprovado=True)
            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Solicitação de Reserva foi Aprovada</h1>
                <p>Sua solicitação de reserva do <strong>{valores[0]}</strong> pro dia <strong>{str(valores[1])[9:10]}/{str(valores[1])[6:7]}</strong> até <strong>{str(valores[1])[9:10]}/{str(valores[1])[6:7]}</strong> horário: <strong>{str(valores[3])[:5]}</strong> até <strong>{str(valores[3])[:5]}</strong> foi <strong>Aprovada</strong></p>""",
                None,
                [valores[5]])
            msg.content_subtype="html"
            msg.send()
            messages.success(request, 'Aprovado')
        else:
            Carro.objects.filter(id=id).update(aprovado=False)
            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Solicitação de Reserva foi Reprovada</h1>
                            <p>Sua solicitação de reserva do <strong>{valores[0]}</strong> pro dia <strong>{str(valores[1])[9:10]}/{str(valores[1])[6:7]}</strong> até <strong>{str(valores[1])[9:10]}/{str(valores[1])[6:7]}</strong> horário: <strong>{str(valores[3])[:5]}</strong> até <strong>{str(valores[3])[:5]}</strong> foi <strong>Reprovada</strong></p>""",
                None,
                [valores[5]])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request, 'Reprovado')
        return redirect('aprovarCarro')
    return render(request,'reserva/aprovarCarro.html',{'db':retorna_soli,'model':model})

def aprovar_sala(request):
    if not request.user.username.endswith('m'):
        return redirect('login')
    if request.user.username.endswith('valdirenem'):
        retorna_soli = Sala.objects.filter(aprovador='Maria Valdirene',aprovado=None)
    else:
        retorna_soli = Sala.objects.filter(aprovador='Mayara Alvarenga',aprovado=None)
    salaObjsTrue = Sala.objects.filter(aprovado=True, dataInit__gte=date.today()).values()
    salaObjsNone = Sala.objects.filter(aprovado=None, dataInit__gte=date.today()).values()
    modelComb = salaObjsNone | salaObjsTrue
    model = modelComb.order_by('-dataInit')
    if request.method =="POST":
        id = request.POST.get('id')
        obj = Carro.objects.filter(id=id).values('carro', 'dataInit', 'dataEnd', 'horaInit', 'horaEnd',
                                                 'email_solicitante')
        valores = []
        for campo, valor in obj[0].items():
            valores.append(valor)
        if request.POST.get('botao') == 'aprovar':
            Sala.objects.filter(id=id).update(aprovado=True)
            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Solicitação de Reserva foi Aprovada</h1>
                            <p>Sua solicitação de reserva da <strong>{valores[0]}</strong> pro dia <strong>{str(valores[1])[9:10]}/{str(valores[1])[6:7]}</strong> até <strong>{str(valores[1])[9:10]}/{str(valores[1])[6:7]}</strong> horário: <strong>{str(valores[3])[:5]}</strong> até <strong>{str(valores[3])[:5]}</strong> foi <strong>Aprovada</strong></p>""",
                None,
                [valores[5]])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request,'Aprovado')
        else:
            Sala.objects.filter(id=id).update(aprovado=False)
            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Solicitação de Reserva foi Reprovada</h1>
                            <p>Sua solicitação de reserva da <strong>{valores[0]}</strong> pro dia <strong>{str(valores[1])[9:10]}/{str(valores[1])[6:7]}</strong> até <strong>{str(valores[1])[9:10]}/{str(valores[1])[6:7]}</strong> horário: <strong>{str(valores[3])[:5]}</strong> até <strong>{str(valores[3])[:5]}</strong> foi <strong>Reprovada</strong></p>""",
                None,
                [valores[5]])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request, 'Reprovado')
        return redirect('aprovarSala')
    return render(request,'reserva/aprovarSala.html',{'db':retorna_soli,'model':model})