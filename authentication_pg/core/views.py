from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
import re
from django.shortcuts import redirect
from . import emails
from django.contrib.auth.decorators import login_required
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
        senha = request.POST.get('senha', '')

        for campo, valor in request.POST.items():
            if campo == 'csrfmiddlewaretoken':
                continue

            if not valor.strip():
                vazio[campo] = True

        if vazio:
            check = False
            return render(request, 'core/login.html', {
                'vazio': vazio,
                'dados': request.POST
                })
        
        if check == True:
            new_user = authenticate(request, username=email, password=senha)
            if new_user:
                login(request, new_user)
                return HttpResponse('vc está autenticado')
            
            aviso = 1
            return render(request, 'core/login.html', {'aviso':aviso})
            
            
        
    return render(request, 'core/login.html')

def verifica_email(request):
    if request.method == 'POST':
        aviso = 0
        email_recup = request.POST.get('email', '').strip()

        if User.objects.filter(email=email_recup).exists():
            codigo_valid = emails.send_email(email_recup)
            request.session['codigo_valid'] = codigo_valid
            request.session['email_recup'] = email_recup
            return redirect('redefinir')

        aviso = 1
        return render(request, 'core/email.html', {'aviso':aviso})
    return render(request, 'core/email.html')

def redefinir(request):
    if request.method == 'POST':

        aviso = 0
        codigo_user = request.POST.get('codigo', '')
        codigo_valid = request.session.get('codigo_valid')
        
        if codigo_user == codigo_valid:
            return redirect('trocarsenha')
        aviso = 1
        return render(request, 'core/redefinir.html', {'aviso':aviso})

    return render(request, 'core/redefinir.html')

def trocarsenha(request):
    if request.method == 'POST':

        check = True
        aviso = 0
        vazio = {}
        
        new_senha1 = request.POST.get('senha1', '')
        new_senha2 = request.POST.get('senha2', '')

        for campo, valor in request.POST.items():
            if campo == 'csrfmiddlewaretoken':
                continue

            if not valor.strip():
                vazio[campo] = True

        if vazio:
            check = False
            return render(request, 'core/trocarsenha.html', {
                'vazio': vazio,
                'dados': request.POST
                })

        if not (8 <= len(new_senha1) <= 12):
            check = False
            aviso = 2
            return render(request, 'core/trocarsenha.html', {'aviso':aviso})
        
        if not re.search(r"[A-Za-z]", new_senha1) or not re.search(r"[0-9]", new_senha1):
            check = False
            aviso = 3
            return render(request, 'core/trocarsenha.html', {'aviso':aviso})
        
        if re.match(r'^(?:[^A-Z]*|[^a-z]*)$', new_senha1):
            check = False
            aviso = 4
            return render(request, 'core/trocarsenha.html', {'aviso':aviso})

        if new_senha1 != new_senha2:
            check = False
            aviso = 5
            return render(request, 'core/trocarsenha.html', {'aviso':aviso})

        if request.user.check_password(new_senha1):
            check = False
            aviso = 6
            return render(request, 'core/trocarsenha.html', {'aviso':aviso})

        if check == True:
            request.user.set_password(new_senha1)
            request.user.save()
            return redirect('index')
   
    return render(request, 'core/trocarsenha.html')