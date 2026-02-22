from django.urls import path
from .  import views

urlpatterns = [
    path('', views.base, name='base'),
    path('index/', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login_user, name='login'),
    path('redefinir/', views.redefinir, name='redefinir'),
    path('email/', views.verifica_email, name='email'),
    path('trocarsenha/', views.trocarsenha, name='trocarsenha'),
]