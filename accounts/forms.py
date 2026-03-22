import re
from django import forms
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class EditarPerfilForm(forms.ModelForm):
    """
    Formulário para atualização de dados básicos do perfil do usuário logado.
    Permite apenas a edição de informações não sensíveis.
    """
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'foto']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control form-control-sm'}),
        }
        
class ColaboradorForm(forms.ModelForm):
    """
    Formulário principal para cadastro e edição de colaboradores e usuários do sistema.
    Implementa regras de validação de CPF e controle de nível de acesso (RBAC).
    """
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'cpf', 'matricula', 'email', 'perfil', 'foto', 'data_vencimento_aso']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 12345678901'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matrícula'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@empresa.com'}),
            'perfil': forms.Select(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'data_vencimento_aso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Sobrescreve a inicialização para aplicar regras de negócio dinâmicas.
        Restringe as opções de perfil caso o usuário logado seja da equipe de SST.
        """
        logged_user = kwargs.pop('logged_user', None)
        super().__init__(*args, **kwargs)
        
        if logged_user and logged_user.perfil == 'SST':
            self.fields['perfil'].choices = [('COLABORADOR', 'Colaborador')]

    def clean_cpf(self):
        """
        Sanitiza o campo CPF inserido pelo usuário, removendo máscaras (pontos e traços)
        para garantir que apenas os 11 dígitos numéricos sejam persistidos no banco.
        """
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            cpf = re.sub(r'[^0-9]', '', cpf)
        return cpf

    def save(self, commit=True):
        """
        Intercepta o salvamento do formulário para espelhar o CPF sanitizado
        no campo 'username', garantindo o funcionamento nativo da autenticação do Django.
        """
        user = super().save(commit=False)
        
        if hasattr(user, 'username'):
            user.username = user.cpf
            
        if commit:
            user.save()
        return user