from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator

class MeuUsuarioManager(UserManager):
    """
    Gerenciador customizado para o modelo de Usuário.
    Garante que regras de negócio específicas sejam aplicadas na criação de usuários.
    """
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Sobrescreve a criação de superusuário para garantir que, por padrão,
        ele seja classificado com o perfil de 'ADMIN' no sistema (RBAC).
        """
        extra_fields.setdefault('perfil', 'ADMIN')
        return super().create_superuser(username, email, password, **extra_fields)

class Usuario(AbstractUser):
    """
    Modelo de Usuário customizado do sistema EPI-System.
    Substitui o modelo padrão do Django para incluir dados de identificação corporativa
    e controle de saúde ocupacional (ASO/NR-7).
    """
    
    # Níveis de Acesso (RBAC)
    TIPOS_PERFIL = (
        ('ADMIN', 'Administrador'),
        ('SST', 'Técnico de SST'),
        ('ALMOXARIFE', 'Almoxarife'),
        ('COLABORADOR', 'Colaborador'),
    )
    
    objects = MeuUsuarioManager()

    # Validadores de Dados
    cpf_validator = RegexValidator(
        regex=r'^\d{11}$',
        message='O CPF deve conter exatamente 11 números, sem pontos ou traços.'
    )

    # Campos de Identificação Corporativa
    cpf = models.CharField(
        'CPF', 
        max_length=11, 
        unique=True, 
        validators=[cpf_validator]
    )
    matricula = models.CharField('Matrícula', max_length=20, unique=True)
    perfil = models.CharField('Perfil de Acesso', max_length=20, choices=TIPOS_PERFIL, default='COLABORADOR')
    foto = models.ImageField('Foto de Perfil', upload_to='fotos_perfil/', null=True, blank=True)

    # Controle de Saúde Ocupacional (SST - NR-7)
    data_vencimento_aso = models.DateField('Vencimento do ASO (Exame)', null=True, blank=True)

    def __str__(self):
        """
        Representação em string do objeto, exibindo o nome completo e o cargo formatado.
        """
        return f"{self.first_name} {self.last_name} ({self.get_perfil_display()})"