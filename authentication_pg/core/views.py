from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import tags
from django.http import HttpResponse





# Create your views here.

def base(request):
    return render(request, 'core/base.html')

def index(request):
    return render(request, 'core/index.html')

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha1 = request.POST.get('senha1')
        senha2 = request.POST.get('senha2')
        campo_vazio()

        def campo_vazio(request):
            vazio = {}
            for campo, valor in request.POST.items():
                if campo != 'csrfmiddlewaretoken' and valor.strip() == '':
                    vazio[campo] = True
            return render(request, 'core/cadastro.html', {vazio:'vazio'})
    
        if User.objects.filter(email=email).exists():   
            messages.info(request, 'Já existe uma conta com esse email')
        elif len(senha1) < 8 or len(senha1) > 12:
            return HttpResponse('Ok, sua senha deve ter entre 8 e 12 digitos')
        elif senha1 != senha2:
            return HttpResponse('Ok, suas senhas estão diferentes')
        else:
            return HttpResponse('Ok, aguarde atualizações')
        
    return render(request, 'core/cadastro.html')

def login(request):
    return render(request, 'core/login.html')


