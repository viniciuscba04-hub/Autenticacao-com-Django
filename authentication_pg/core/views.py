from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages




# Create your views here.

def base(request):
    return render(request, 'core/base.html')

def index(request):
    return render(request, 'core/index.html')

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        if User.objects.filter(email=email).exists():   
            messages.info(request, 'Já existe uma conta com esse email')
        
    return render(request, 'core/cadastro.html')

def login(request):
    return render(request, 'core/login.html')


