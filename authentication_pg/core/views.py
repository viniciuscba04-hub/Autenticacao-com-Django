from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
import re
from django.shortcuts import redirect

# Create your views here.

def base(request):
    return render(request, 'core/base.html')

def index(request):
    return render(request, 'core/index.html')

def cadastro(request):
    if request.method == 'POST':

        check = True
        aviso = 0
        vazio = {}

        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip()
        senha1 = request.POST.get('senha1', '')
        senha2 = request.POST.get('senha2', '')

        for campo, valor in request.POST.items():
            if campo == 'csrfmiddlewaretoken':
                continue

            if not valor.strip():
                vazio[campo] = True

        if vazio:
            check = False
            return render(request, 'core/cadastro.html', {
                'vazio': vazio,
                'dados': request.POST
                })

        if User.objects.filter(email=email).exists():
            check = False
            aviso = 1
            return render(request, 'core/cadastro.html', {'aviso':aviso})

        if not (8 <= len(senha1) <= 12):
            check = False
            aviso = 2
            return render(request, 'core/cadastro.html', {'aviso':aviso})
        
        if not re.search(r"[A-Za-z]", senha1) or not re.search(r"[0-9]", senha1):
            check = False
            aviso = 3
            return render(request, 'core/cadastro.html', {'aviso':aviso})
        
        if re.match(r'^(?:[^A-Z]*|[^a-z]*)$', senha1):
            check = False
            aviso = 4
            return render(request, 'core/cadastro.html', {'aviso':aviso})

        if senha1 != senha2:
            check = False
            aviso = 5
            return render(request, 'core/cadastro.html', {'aviso':aviso})
        
        if check == True:
            User.objects.create_user(username=email, first_name=nome, email=email, password=senha1)
            return redirect('login')
        

    return render(request, 'core/cadastro.html')

def login_user(request):
    if request.method == 'POST':

        check = True
        aviso = 0
        vazio = {}

        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '').strip()

        for campo, valor in request.POST.items():
            if campo == 'csrfmiddlewaretoken':
                continue

            if not valor.strip():
                vazio[campo] = True

        if vazio:
            check = False
            return render(request, 'core/cadastro.html', {
                'vazio': vazio,
                'dados': request.POST
                })
        
        if check == True:
            new_user = authenticate(request, username=email, password=senha)
            if new_user:
                login(new_user)
                return render(request, 'core/index.html')
            
            aviso = 1
            return render(request, 'core/login.html', {'aviso':aviso})
            
            
        
    return render(request, 'core/login.html')


