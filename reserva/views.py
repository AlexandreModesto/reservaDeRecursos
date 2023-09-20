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
    carro_list=['FordKa','Onix','HB20']
    sala_list=['Sala Terreo','Sala andar 1','Sala Maior Conad','Sala Menor Conad','Auditório']
    return render(request,'reserva/index.html',{'carro_list':carro_list,'sala_list':sala_list})

def carro(request,result,carro):
    carroForm = ReservaCarro()
    result = result.split('-')
    print(carro)
    data = f'{result[0]}/{result[1]}/{result[2]}'
    n_result = f'{result[2]}/{result[1]}/{result[0]}'
    if request.method == 'POST':
        carroForm = ReservaCarro(request.POST)
        if carroForm.is_valid():
            nome=carroForm.cleaned_data['nome']
            email=carroForm.cleaned_data['email']
            hora=carroForm.cleaned_data['horas']
            rep=carroForm.cleaned_data['repetir']


            data_f = datetime.strptime(n_result, '%Y/%m/%d').date()
            if not rep:
                print(data_f)
                r=Carro(carro=carro,solicitante=nome,email_solicitante=email,data=data_f,hora=hora)
                # r.save()
            else:
                nuRepetir = request.POST.get('nuRepetir', None)  # numero
                tpRepetir = request.POST.get('tpRepetir', None)  # D/S
                ate = request.POST.get('ate', None)
                print()
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
                                            <p><strong>{nome} esta solicitando reserva do {carro} pro dia <strong>{data}</strong> horário: <strong>{hora}</strong></p>
                                            <p>Para aprovar ou não clique <a href='10.110.209.15/aprovarSala'>aqui</a></p>""",
                None,
                ['xandy.modest14@gmail.com'])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request,'Reserva encaminhada para Aprovação')
            return redirect('index')
        print(carroForm.errors.as_data())
    return render(request,'reserva/carro.html',{'carroForm':carroForm,'carro':carro,'data':data})

def sala(request,result,sala):
    salaForm = ReservaSala()
    result = result.split('-')
    print(sala)
    data = f'{result[0]}/{result[1]}/{result[2]}'
    n_result = f'{result[2]}/{result[1]}/{result[0]}'
    if request.method == 'POST':
        salaForm = ReservaSala(request.POST)
        if salaForm.is_valid():
            nome=salaForm.cleaned_data['nome']
            email=salaForm.cleaned_data['email']
            hora=salaForm.cleaned_data['horas']
            rep=salaForm.cleaned_data['repetir']


            data_f = datetime.strptime(n_result, '%Y/%m/%d').date()
            if not rep:
                print(data_f)
                r=Sala(sala=sala,solicitante=nome,email_solicitante=email,data=data_f,hora=hora)
                r.save()
            else:
                nuRepetir = request.POST.get('nuRepetir', None)  # numero
                tpRepetir = request.POST.get('tpRepetir', None)  # D/S
                ate = request.POST.get('ate', None)
                print()
                ate_f = datetime.strptime(ate, '%Y-%m-%d').date()

                prox_data = data_f
                if tpRepetir == 'D':
                    print(prox_data)
                    r = Sala(sala=sala, solicitante=nome, email_solicitante=email,
                              data=str(prox_data), hora=hora)
                    r.save()
                    for i in range(0,(ate_f.day-data_f.day)+1, int(nuRepetir)):
                        prox_data=prox_data + timedelta(days=int(nuRepetir))
                        if prox_data > ate_f:
                            break
                        print(prox_data)
                        r = Sala(sala=sala, solicitante=nome, email_solicitante=email,
                                  data=str(prox_data), hora=hora)
                        r.save()
                else:
                    print(prox_data)
                    r = Sala(sala=sala, solicitante=nome, email_solicitante=email,
                              data=str(prox_data), hora=hora)
                    r.save()
                    finalRange = ate_f - data_f
                    for i in range(7, finalRange.days+1,7):
                        prox_data = prox_data + timedelta(weeks=int(nuRepetir))
                        if prox_data > ate_f:
                            break
                        print(prox_data)
                        r = Sala(sala=sala, solicitante=nome, email_solicitante=email,
                                  data=str(prox_data), hora=hora)
                        r.save()

            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Nova Solicitação de Reserva</h1>
                                            <p><strong>{nome} esta solicitando reserva da(o) {sala} pro dia <strong>{data}</strong> horário: <strong>{hora}</strong></p>
                                            <p>Para aprovar ou não clique <a href='10.110.209.15/aprovarSala'>aqui</a></p>""",
                None,
                ['xandy.modest14@gmail.com'])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request,'Reserva encaminhada para Aprovação')
            return redirect('index')
        print(salaForm.errors.as_data())
    return render(request,'reserva/sala.html',{'salaForm':salaForm,'sala':sala,'data':data})


def login(request):
    if request.user.is_authenticated:
        if not request.user.username.endswith('m'):
            return redirect('aprovarCarro')
        else:return redirect('aprovarSala')
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
    retorna_soli_none = Carro.objects.filter(aprovado=None,data__gte=datetime.today())
    retorna_soli_true = Carro.objects.filter(aprovado=True,data__gte=datetime.today())
    retorna_soli=retorna_soli_none | retorna_soli_true

    if request.method =="POST":
        check = request.POST.get('botao')
        id = request.POST.get('id')
        obj = Carro.objects.filter(id=id).values('carro','data','hora','email_solicitante')
        valores=[]
        for campo,valor in obj[0].items():
            valores.append(valor)

        if check == 'aprovar':
            Carro.objects.filter(id=id).update(aprovado=True)
            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Solicitação de Reserva foi Aprovada</h1>
                <p>Sua solicitação de reserva do <strong>{valores[0]}</strong> pro dia <strong>{str(valores[1])[8:10]}/{str(valores[1])[5:7]}/{str(valores[1])[:4]}</strong> horário: <strong>{valores[2]}</strong> foi <strong>Aprovada</strong></p>""",
                None,
                [valores[3]])
            msg.content_subtype="html"
            msg.send()
            messages.success(request, 'Aprovado')
        elif check == 'cancelar':
            Carro.objects.filter(id=id).update(aprovado=False)
            parecer=request.POST.get('reproCancelado')
            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Solicitação de Reserva foi Cancelada</h1>
                <p>Sua solicitação de reserva do <strong>{valores[0]}</strong> pro dia <strong>{str(valores[1])[8:10]}/{str(valores[1])[5:7]}/{str(valores[1])[:4]}</strong> horário: <strong>{valores[2]}</strong> foi <strong>Cancelada</strong></p>
                <p><strong>Motivo</strong>: {parecer}</p>""",
                None,
                [valores[3]])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request, 'Cancelado')
        else:
            Carro.objects.filter(id=id).update(aprovado=False)
            parecer=request.POST.get('repro')
            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Solicitação de Reserva foi Reprovada</h1>
                <p>Sua solicitação de reserva do <strong>{valores[0]}</strong> pro dia <strong>{str(valores[1])[8:10]}/{str(valores[1])[5:7]}/{str(valores[1])[:4]}</strong> horário: <strong>{valores[2]}</strong> foi <strong>reprovada</strong></p>
                <p><strong>Motivo</strong>: {parecer}</p>""",
                None,
                [valores[3]])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request, 'Reprovado')
        return redirect('aprovarCarro')
    return render(request,'reserva/aprovarCarro.html',{'db':retorna_soli})

def aprovar_sala(request):
    if not request.user.username.endswith('m'):
        return redirect('login')
    mayara='Mayara Alvarenga'
    vald='Maria Valdirene'
    maze='Maria José'
    if request.user.username.endswith('valdirenem'):
        retorna_soli = Sala.objects.filter(aprovador=vald,aprovado=None,data__gte=date.today())
    elif request.user.username.endswith('teixeiram'):
        retorna_soli = Sala.objects.filter(aprovador=maze,aprovado=None,data__gte=date.today())
    else:
        retorna_soli = Sala.objects.filter(aprovador=mayara,aprovado=None,data__gte=date.today())

    if request.method =="POST":
        id = request.POST.get('id')
        check = request.POST.get('botao')
        obj = Sala.objects.filter(id=id).values('sala', 'data','hora','email_solicitante')
        valores = []
        for campo, valor in obj[0].items():
            valores.append(valor)
        if check == 'aprovar':
            Sala.objects.filter(id=id).update(aprovado=True)
            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Solicitação de Reserva foi Aprovada</h1>
                <p>Sua solicitação de reserva do <strong>{valores[0]}</strong> pro dia <strong>{str(valores[1])[8:10]}/{str(valores[1])[5:7]}/{str(valores[1])[:4]}</strong> horário: <strong>{valores[2]}</strong> foi <strong>Aprovada</strong></p>""",
                None,
                [valores[3]])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request, 'Aprovado')
        elif check == 'cancelar':
            Sala.objects.filter(id=id).update(aprovado=False)
            parecer = request.POST.get('reproCancelado')
            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Solicitação de Reserva foi Cancelada</h1>
                <p>Sua solicitação de reserva do <strong>{valores[0]}</strong> pro dia <strong>{str(valores[1])[8:10]}/{str(valores[1])[5:7]}/{str(valores[1])[:4]}</strong> horário: <strong>{valores[2]}</strong> foi <strong>Cancelada</strong></p>
                <p><strong>Motivo</strong>: {parecer}</p>""",
                None,
                [valores[3]])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request, 'Cancelado')
        else:
            Sala.objects.filter(id=id).update(aprovado=False)
            parecer = request.POST.get('repro')
            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Solicitação de Reserva foi Reprovada</h1>
                <p>Sua solicitação de reserva do <strong>{valores[0]}</strong> pro dia <strong>{str(valores[1])[8:10]}/{str(valores[1])[5:7]}/{str(valores[1])[:4]}</strong> horário: <strong>{valores[2]}</strong> foi <strong>reprovada</strong></p>
                <p><strong>Motivo</strong>: {parecer}</p>""",
                None,
                [valores[3]])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request, 'Reprovado')
        return redirect('aprovarSala')
    return render(request,'reserva/aprovarSala.html',{'db':retorna_soli})

def return_number(mes):
    dict = {'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4, 'Maio': 5, 'Junho': 6, 'Julho': 7,
            'Agosto': 8, 'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12}
    return dict[mes]

def reservas(request,item):
    form=ReservasForm()
    if request.method =='POST':
        result = request.POST.get('result',None)
        result = result.replace('/','-')
        if item[:4] == 'Sala' or item == 'Auditorio':
            return redirect('salas', result, item)
        else:
            return redirect('carros',result,item)
    return render(request,'reserva/reservas.html',{'item':item})

def reservas_get(request,carro,dat):
    tabela=Carro.objects.filter(data=dat,carro=carro).values()
    table = {'solicitante':'', 'motivo':'', 'hora':''}
    for item in tabela:
        table['solicitante']+=' '+item['solicitante']
        table['motivo'] += ' '+str(item['motivo'])
        table['hora'] += ' '+item['hora']
    table['solicitante'] = table['solicitante'].split()
    table['motivo'] = table['motivo'].split()
    table['hora'] = table['hora'].split()
    return JsonResponse(table,safe=False)

def reservas_json(request,item):
    consultaSala = Sala.objects.filter(data__gte=datetime.today())
    consultaCarro = Carro.objects.filter(data__gte=datetime.today())

    #Ford Ka

    if item == 'FordKa':
        indice = 0
        fordka=consultaCarro.filter(carro='FordKa')
        resultadosFordKa = {}
        mes_anterior=''

        for i in range(0,len(fordka.dates('data','month'))):
            dias = []
            datas = []
            motivo = []
            solicitante = []
            aux=fordka.order_by('data').values()
            while True:
                aux_date=aux[indice]['data']
                mes=datetime.strptime(str(aux_date),'%Y-%m-%d').date().month

                if not mes == mes_anterior :
                    print(datetime.strptime(str(aux_date), '%Y-%m-%d').date(), mes)
                    mes_anterior=mes
                    break
                else:
                    indice+=1

            for item in fordka.filter(data__month=mes):
                data = datetime.strptime(str(item.data),'%Y-%m-%d').date()
                dias.append(data.day)
                data_f= str(data).split('-')
                data_s=f'{data_f[2]}/{data_f[1]}/{data_f[0]}'
                datas.append(data_s)

                motivo.append(item.motivo)
                solicitante.append(item.solicitante)

            dados={
                "mes":mes-1,
                "dia":dias,
                "datas":datas,
                "motivo":motivo,
                "solicitante":solicitante
            }
            resultadosFordKa[i]=dados

        return JsonResponse(resultadosFordKa)

    #Onix

    elif item == 'Onix':
        indice = 0
        onix = consultaCarro.filter(carro='Onix')
        resultadosOnix = {}
        mes_anterior = ''

        for i in range(0, len(onix.dates('data', 'month'))):
            dias = []
            datas = []
            motivo = []
            solicitante = []
            aux = onix.order_by('data').values()
            while True:
                aux_date = aux[indice]['data']
                mes = datetime.strptime(str(aux_date), '%Y-%m-%d').date().month

                if not mes == mes_anterior:
                    print(datetime.strptime(str(aux_date), '%Y-%m-%d').date(), mes)
                    mes_anterior = mes
                    break
                else:
                    indice += 1

            for item in onix.filter(data__month=mes):
                data = datetime.strptime(str(item.data), '%Y-%m-%d').date()
                dias.append(data.day)
                data_f = str(data).split('-')
                data_s = f'{data_f[2]}/{data_f[1]}/{data_f[0]}'
                datas.append(data_s)

                motivo.append(item.motivo)
                solicitante.append(item.solicitante)

            dados = {
                "mes": mes - 1,
                "dia": dias,
                "datas": datas,
                "motivo": motivo,
                "solicitante": solicitante
            }
            resultadosOnix[i] = dados

        return JsonResponse(resultadosOnix)

    #HB20

    elif item == 'HB20':
        indice = 0
        HB20 = consultaCarro.filter(carro='HB20')
        resultadosHB20 = {}
        mes_anterior = ''

        for i in range(0, len(HB20.dates('data', 'month'))):
            dias = []
            datas = []
            motivo = []
            solicitante = []
            aux = HB20.order_by('data').values()
            while True:
                aux_date = aux[indice]['data']
                mes = datetime.strptime(str(aux_date), '%Y-%m-%d').date().month

                if not mes == mes_anterior:
                    print(datetime.strptime(str(aux_date), '%Y-%m-%d').date(), mes)
                    mes_anterior = mes
                    break
                else:
                    indice += 1

            for item in HB20.filter(data__month=mes):
                data = datetime.strptime(str(item.data), '%Y-%m-%d').date()
                dias.append(data.day)
                data_f = str(data).split('-')
                data_s = f'{data_f[2]}/{data_f[1]}/{data_f[0]}'
                datas.append(data_s)

                motivo.append(item.motivo)
                solicitante.append(item.solicitante)

            dados = {
                "mes": mes - 1,
                "dia": dias,
                "datas": datas,
                "motivo": motivo,
                "solicitante": solicitante
            }
            resultadosHB20[i] = dados

        return JsonResponse(resultadosHB20)

    #Sala andar 1

    elif item == 'Sala andar 1':
        indice = 0
        sala1 = consultaSala.filter(sala='Sala andar 1')
        resultadosSala1 = {}
        mes_anterior = ''

        for i in range(0, len(sala1.dates('data', 'month'))):
            dias = []
            datas = []
            motivo = []
            solicitante = []
            aux = sala1.order_by('data').values()
            while True:
                aux_date = aux[indice]['data']
                mes = datetime.strptime(str(aux_date), '%Y-%m-%d').date().month

                if not mes == mes_anterior:
                    print(datetime.strptime(str(aux_date), '%Y-%m-%d').date(), mes)
                    mes_anterior = mes
                    break
                else:
                    indice += 1

            for item in sala1.filter(data__month=mes):
                data = datetime.strptime(str(item.data), '%Y-%m-%d').date()
                dias.append(data.day)
                data_f = str(data).split('-')
                data_s = f'{data_f[2]}/{data_f[1]}/{data_f[0]}'
                datas.append(data_s)

                motivo.append(item.motivo)
                solicitante.append(item.solicitante)

            dados = {
                "mes": mes - 1,
                "dia": dias,
                "datas": datas,
                "motivo": motivo,
                "solicitante": solicitante
            }
            resultadosSala1[i] = dados

        return JsonResponse(resultadosSala1)

    #Sala Terreo

    elif item == 'Sala Terreo':
        indice = 0
        salaT = consultaSala.filter(sala='Sala Terreo')
        resultadosSalaT = {}
        mes_anterior = ''

        for i in range(0, len(salaT.dates('data', 'month'))):
            dias = []
            datas = []
            motivo = []
            solicitante = []
            aux = salaT.order_by('data').values()
            while True:
                aux_date = aux[indice]['data']
                mes = datetime.strptime(str(aux_date), '%Y-%m-%d').date().month

                if not mes == mes_anterior:
                    print(datetime.strptime(str(aux_date), '%Y-%m-%d').date(), mes)
                    mes_anterior = mes
                    break
                else:
                    indice += 1

            for item in salaT.filter(data__month=mes):
                data = datetime.strptime(str(item.data), '%Y-%m-%d').date()
                dias.append(data.day)
                data_f = str(data).split('-')
                data_s = f'{data_f[2]}/{data_f[1]}/{data_f[0]}'
                datas.append(data_s)

                motivo.append(item.motivo)
                solicitante.append(item.solicitante)

            dados = {
                "mes": mes - 1,
                "dia": dias,
                "datas": datas,
                "motivo": motivo,
                "solicitante": solicitante
            }
            resultadosSalaT[i] = dados

        return JsonResponse(resultadosSalaT)

    #Sala Conad Maior

    elif item == 'Sala Conad Maior':
        indice = 0
        salaConadM = consultaSala.filter(sala='Sala Conad Maior')
        resultadosSalaConadM = {}
        mes_anterior = ''

        for i in range(0, len(salaConadM.dates('data', 'month'))):
            dias = []
            datas = []
            motivo = []
            solicitante = []
            aux = salaConadM.order_by('data').values()
            while True:
                aux_date = aux[indice]['data']
                mes = datetime.strptime(str(aux_date), '%Y-%m-%d').date().month

                if not mes == mes_anterior:
                    print(datetime.strptime(str(aux_date), '%Y-%m-%d').date(), mes)
                    mes_anterior = mes
                    break
                else:
                    indice += 1

            for item in salaConadM.filter(data__month=mes):
                data = datetime.strptime(str(item.data), '%Y-%m-%d').date()
                dias.append(data.day)
                data_f = str(data).split('-')
                data_s = f'{data_f[2]}/{data_f[1]}/{data_f[0]}'
                datas.append(data_s)

                motivo.append(item.motivo)
                solicitante.append(item.solicitante)

            dados = {
                "mes": mes - 1,
                "dia": dias,
                "datas": datas,
                "motivo": motivo,
                "solicitante": solicitante
            }
            resultadosSalaConadM[i] = dados

        return JsonResponse(resultadosSalaConadM)

    #Sala Conad Menor

    elif item == 'Sala Conad Menor':
        indice = 0
        salaConadm = consultaSala.filter(sala='Sala Conad Menor')
        resultadosSalaConadm = {}
        mes_anterior = ''

        for i in range(0, len(salaConadm.dates('data', 'month'))):
            dias = []
            datas = []
            motivo = []
            solicitante = []
            aux = salaConadm.order_by('data').values()
            while True:
                aux_date = aux[indice]['data']
                mes = datetime.strptime(str(aux_date), '%Y-%m-%d').date().month

                if not mes == mes_anterior:
                    print(datetime.strptime(str(aux_date), '%Y-%m-%d').date(), mes)
                    mes_anterior = mes
                    break
                else:
                    indice += 1

            for item in salaConadm.filter(data__month=mes):
                data = datetime.strptime(str(item.data), '%Y-%m-%d').date()
                dias.append(data.day)
                data_f = str(data).split('-')
                data_s = f'{data_f[2]}/{data_f[1]}/{data_f[0]}'
                datas.append(data_s)

                motivo.append(item.motivo)
                solicitante.append(item.solicitante)

            dados = {
                "mes": mes - 1,
                "dia": dias,
                "datas": datas,
                "motivo": motivo,
                "solicitante": solicitante
            }
            resultadosSalaConadm[i] = dados

        return JsonResponse(resultadosSalaConadm)

    #Auditorio

    else:
        indice = 0
        salaAuditorio = consultaSala.filter(sala='Auditorio')
        resultadosSalaAuditorio = {}
        mes_anterior = ''

        for i in range(0, len(salaAuditorio.dates('data', 'month'))):
            dias = []
            datas = []
            motivo = []
            solicitante = []
            aux = salaAuditorio.order_by('data').values()
            while True:
                aux_date = aux[indice]['data']
                mes = datetime.strptime(str(aux_date), '%Y-%m-%d').date().month

                if not mes == mes_anterior:
                    print(datetime.strptime(str(aux_date), '%Y-%m-%d').date(), mes)
                    mes_anterior = mes
                    break
                else:
                    indice += 1

            for item in salaAuditorio.filter(data__month=mes):
                data = datetime.strptime(str(item.data), '%Y-%m-%d').date()
                dias.append(data.day)
                data_f = str(data).split('-')
                data_s = f'{data_f[2]}/{data_f[1]}/{data_f[0]}'
                datas.append(data_s)

                motivo.append(item.motivo)
                solicitante.append(item.solicitante)

            dados = {
                "mes": mes - 1,
                "dia": dias,
                "datas": datas,
                "motivo": motivo,
                "solicitante": solicitante
            }
            resultadosSalaAuditorio[i] = dados

        return JsonResponse(resultadosSalaAuditorio)

def reserva_mes(request,db):
    if not db == 'Sala':
        retorno = Carro.objects.filter(created_at__month__gte=date.today().month)
        retorno_todos = Carro.objects.filter(created_at__month__lte=date.today().month)
        retorno_todos =retorno_todos.filter(created_at__month__gte=date.today().month-2)
        return render(request, 'reserva/reservasCarro.html', {'model': retorno,'model_todos':retorno_todos})
    else:
        retorno = Sala.objects.filter(created_at__month__gte=date.now().month)
        retorno_todos = Sala.objects.filter(created_at__month__lte=date.today().month)
        retorno_todos = retorno_todos.filter(created_at__month__gte=date.today().month - 2)
        return render(request, 'reserva/reservasSala.html', {'model': retorno,'model_todos':retorno_todos})

