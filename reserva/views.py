#-*-coding:utf-8 -*-
import django.contrib.auth
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate
from .models import Carro,Sala
from .forms import ReservaSala,ReservaCarro,LoginForms,ReservasForm
from django.core.mail import EmailMessage
from django.contrib import messages
from datetime import date,datetime,timedelta


def index(request):
    return render(request,'reserva/index.html')

def carro(request,result,carro):
    carroForm = ReservaCarro()

    if request.method == 'POST':
        carroForm = ReservaCarro(request.POST)
        if carroForm.is_valid():
            nome=carroForm.cleaned_data['nome']
            email=carroForm.cleaned_data['email']
            hora=carroForm.cleaned_data['horas']
            rep=carroForm.cleaned_data['repetir']
            result = result.split('-')
            n_result = f'{result[2]}/{result[1]}/{result[0]}'

            data_f = datetime.strptime(n_result, '%Y/%m/%d').date()
            if not rep:
                print(data_f)
                r=Carro(carro=carro,solicitante=nome,email_solicitante=email,data=data_f,hora=hora)
                r.save()
            else:
                nuRepetir = request.POST.get('nuRepetir', None)  # numero
                tpRepetir = request.POST.get('tpRepetir', None)  # D/S
                ate = request.POST.get('ate', None)
                ate_f = datetime.strptime(ate, '%Y-%m-%d').date()

                prox_data = data_f
                if tpRepetir == 'D':
                    print(prox_data)
                    r = Carro(carro=carro, solicitante=nome, email_solicitante=email,
                              data=str(prox_data), hora=hora)
                    r.save()
                    for i in range(0,(ate_f.day-data_f.day)+1, int(nuRepetir)):
                        prox_data=prox_data + timedelta(days=int(nuRepetir))
                        if prox_data > ate_f:
                            break
                        print(prox_data)
                        r = Carro(carro=carro, solicitante=nome, email_solicitante=email,
                                  data=str(prox_data), hora=hora)
                        r.save()
                else:
                    print(prox_data)
                    r = Carro(carro=carro, solicitante=nome, email_solicitante=email,
                              data=str(prox_data), hora=hora)
                    r.save()
                    finalRange = ate_f - data_f
                    for i in range(7, finalRange.days+1,7):
                        prox_data = prox_data + timedelta(weeks=int(nuRepetir))
                        if prox_data > ate_f:
                            break
                        print(prox_data)
                        r = Carro(carro=carro, solicitante=nome, email_solicitante=email,
                                  data=str(prox_data), hora=hora)
                        r.save()

            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Nova Solicitação de Reserva</h1>
                                            <p><strong>{nome} esta solicitando reserva de carro pro dia <strong>{result[0]}/{result[1]}/{result[2]}</strong> horário: <strong>{hora}</strong></p>
                                            <p>Para aprovar ou não clique <a href='10.110.209.15/aprovarSala'>aqui</a></p>""",
                None,
                ['xandy.modest14@gmail.com'])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request,'Reserva encaminhada para Aprovação')
            return redirect('index')
        # print(carroForm.errors.as_data())
    return render(request,'reserva/carro.html',{'carroForm':carroForm})

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
            datas=[sala,dataInit,dataEnd,nome,email]
        return redirect('sala_pt_2',datas)
    return render(request, 'reserva/sala.html', {'salaForm': salaForm, 'model': model})

# def sala_pt_2(request,datas):
#     if request.method == 'POST':
#         sala = datas[0]
#         dataInit = datas[1]
#         dataEnd = datas[2]
#         nome = datas[3]
#         email = datas[4]
#         form =
#         if form.is_valid():
#             horaInit = form.cleaned_data['horaInit']
#             horaEnd = form.cleaned_data['horaEnd']
#             if sala=='Sala Conad Menor' or sala=='Sala Conad Maior':
#                 apro='Maria Valdirene'
#                 mail='valdirene.monteiro@sicoob.com.br'
#             elif sala == 'Auditório':
#                 apro='Maria José'
#                 mail='maze.teixeira@sicoob.com.br'
#             else:
#                 apro = 'Mayara Alvarenga'
#                 mail = 'mayara.alvarenga@sicoob.com.br'
#             checador_de_datas('Sala',sala,dataInit,dataEnd,horaInit)
#             s=Sala(sala=sala,aprovador=apro,email=mail,solicitante=nome,email_solicitante=email,dataInit=dataInit,dataEnd=dataEnd,horaEnd=horaEnd,horaInit=horaInit)
#             s.save()
#             msg = EmailMessage(
#                 "Solicitação de Reserva",
#                 fr"""<h1>Nova Solicitação de Reserva</h1>
#                                     <p><strong>{nome} esta solicitando reserva do(a) {sala} pro dia <strong>{dataInit}</strong> até <strong>{dataEnd}</strong> horário: <strong>{horaInit}</strong> até <strong>{horaEnd}</strong></p>
#                                     <p>Para aprovar ou não clique <a href='10.110.209.15/aprovarSala'>aqui</a></p>""",
#                 None,
#                 ['teste@gmail.com'])
#             msg.content_subtype = "html"
#             msg.send()
#             messages.success(request, 'Reserva encaminhada para Aprovação')
#             return redirect('index')


def login(request):
    # if request.user.is_authenticated:
    #     if not request.user.username.endswith('m'):
    #         return redirect('aprovarCarro')
    #     else:return redirect('aprovarSala')
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
    if not request.user.username.endswith('a'):
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
            parecer=request.POST.get('repro')
            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Solicitação de Reserva foi Reprovada</h1>
                            <p>Sua solicitação de reserva do <strong>{valores[0]}</strong> pro dia <strong>{str(valores[1])[9:10]}/{str(valores[1])[6:7]}</strong> até <strong>{str(valores[1])[9:10]}/{str(valores[1])[6:7]}</strong> horário: <strong>{str(valores[3])[:5]}</strong> até <strong>{str(valores[3])[:5]}</strong> foi <strong>Reprovada</strong></p>
                            <p><strong>Motivo</strong>: {parecer}""",
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
    mayara='Mayara Alvarenga'
    vald='Maria Valdirene'
    maze='Maria José'
    aprovador=''
    if request.user.username.endswith('valdirenem'):
        aprovador='Maria Valdirene'
        retorna_soli = Sala.objects.filter(aprovador=aprovador,aprovado=None)
    elif request.user.username.endswith('teixeiram'):
        aprovador = 'Maria José'
        retorna_soli = Sala.objects.filter(aprovador=aprovador,aprovado=None)
    else:
        aprovador='Mayara Alvarenga'
        retorna_soli = Sala.objects.filter(aprovador=aprovador,aprovado=None)
    salaObjsTrue = Sala.objects.filter(aprovado=True, aprovador=aprovador, dataInit__gte=date.today()).values()
    salaObjsNone = Sala.objects.filter(aprovado=None, aprovador=aprovador, dataInit__gte=date.today()).values()
    modelComb = salaObjsNone | salaObjsTrue
    model = modelComb.order_by('-dataInit')
    if request.method =="POST":
        id = request.POST.get('id')
        obj = Sala.objects.filter(id=id).values('sala', 'dataInit', 'dataEnd', 'horaInit', 'horaEnd',
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

def return_number(mes):
    dict = {'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4, 'Maio': 5, 'Junho': 6, 'Julho': 7,
            'Agosto': 8, 'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12}
    return dict[mes]

def reservas(request,mes):
    form=ReservasForm()
    if request.method =='POST':
        result = request.POST.get('result',None)
        result = result.replace('/','-')
        return redirect('carros',result,carro)
    return render(request,'reserva/reservas.html')

def reservas_json(request):
    resultados = {0: {
                        "mes":9,
                        "dia":[4,5,6],
                        "datas":["04/10/2023","05/10/2023","06/10/2023"],
                        "motivo":["motivo 04/10/2023","motivo 05/10/2023","motivo 06/10/2023"],
                        "autor":["autor1","autor2","autor3"]
                      },
                  1: {
                        "mes":8,
                        "dia":[11,12],
                        "datas":["11/09/2023","12/09/2023"],
                        "motivo":["motivo 11/09/2023","motivo 12/09/2023"],
                        "autor":["autor1","autor2"]
                     }
                  }
    return JsonResponse(resultados)
def reserva_mes(request,db,mes):
    if not db == 'Sala':
        retorno = Carro.objects.filter(dataEnd__month__lte=return_number(mes))
        retorno = retorno.filter(dataEnd__month__gte=return_number(mes))
        return render(request, 'reserva/reservasCarro.html', {'model': retorno})
    else:
        retorno = Sala.objects.filter(dataEnd__month__lte=return_number(mes))
        retorno = retorno.filter(dataEnd__month__gte=return_number(mes))
        return render(request, 'reserva/reservasSala.html', {'model': retorno})

def checador_de_datas(db,obj,dataInit,dataEnd,horaInit):
    if not db == 'Sala':
        try:
            busca = Carro.objects.filter(carro=obj,dataInit=dataInit,dataEnd=dataEnd,horaInit__gte=horaInit).filter(horaEnd__lte=horaInit)
        except:
            print('nao tem')
        else:
            print(busca[0][0])
    else:
        busca = Sala.objects.filter(sala=obj,dataInit=dataInit,dataEnd=dataEnd,horaInit__lte=horaInit).filter(horaEnd__gte=horaInit).values()
        try:
            busca[0]
        except:
            print('erro')
        else:
            print(busca[0])
