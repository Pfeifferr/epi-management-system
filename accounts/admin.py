from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class CustomUserAdmin(UserAdmin):
    """
    Configuração do painel administrativo para o modelo de Usuário customizado.
    Estende o UserAdmin padrão do Django para incluir os campos específicos 
    de controle do sistema (CPF, Matrícula, Perfil).
    """
    
    # Configurações de listagem e filtragem no painel
    list_display = ('username', 'first_name', 'last_name', 'perfil', 'is_active')
    list_filter = ('perfil', 'is_active')
    
    # Organização dos campos na tela de edição de usuário
    fieldsets = UserAdmin.fieldsets + (
        ('Dados do Colaborador', {'fields': ('cpf', 'matricula', 'perfil', 'foto')}),
    )
    
    # Organização dos campos na tela de criação de um novo usuário
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Dados do Colaborador', {'fields': ('first_name', 'last_name', 'cpf', 'matricula', 'perfil')}),
    )

admin.site.register(Usuario, CustomUserAdmin)