from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Gestão de Perfil e Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/mudar-senha/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/mudar_senha.html',
        success_url=reverse_lazy('dashboard')
    ), name='mudar_senha'),
    
    # Gestão de Colaboradores (Controle de Acesso SST/Administrativo)
    path('colaboradores/', views.listar_colaboradores, name='listar_colaboradores'),
    path('colaboradores/novo/', views.cadastrar_colaborador, name='cadastrar_colaborador'),
    path('colaboradores/editar/<int:id>/', views.editar_colaborador, name='editar_colaborador'),
    path('colaboradores/deletar/<int:id>/', views.deletar_colaborador, name='deletar_colaborador'),
]