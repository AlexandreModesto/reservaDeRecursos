#-*-coding:utf-8 -*-
from django import forms

class ReservaCarro(forms.Form):
    carroChoices=(('Ford Ka','Ford Ka'),('Onix','Onix'),('HB20','HB20'),)
    carro=forms.ChoiceField(choices=carroChoices,label='Qual carro?')
    nome = forms.CharField(label='Digite seu nome', max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome sobrenome', }))
    email = forms.EmailField(label='Digite seu email', max_length=100,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@email.com'}))

class ReservaSala(forms.Form):
    salaChoices=(('Sala Terreo','Sala no Terreo'),('Sala andar 1','Sala do 1°andar'),('Sala Conad Maior','Sala Maior do Conad'),('Sala Conad Menor','Sala Menor do Conad'))
    salas=forms.ChoiceField(choices=salaChoices,label='Qual sala?')
    nome = forms.CharField(label='Digite seu nome', max_length=100,
                           widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nome sobrenome',}))
    email = forms.EmailField(label='Digite seu email', max_length=100,
                             widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'email@email.com'}))

class LoginForms(forms.Form):
    usuario=forms.CharField(label='Usuario', max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'similar a VPN',}))
    senha=forms.CharField(label='Senha', max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'senha',}))

