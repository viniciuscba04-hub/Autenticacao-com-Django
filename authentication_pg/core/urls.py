from django.urls import path
from .  import views

urlpatterns = [
    path('', views.base, name='base'),
    path('index/', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
]