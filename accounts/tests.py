from django.test import TestCase
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class UsuarioTestCase(TestCase):
    """
    Suíte de testes unitários para o modelo de Usuário customizado.
    Verifica a integridade na criação de perfis e a correta atribuição de permissões (RBAC).
    """
    
    def test_criar_usuario_comum(self):
        """
        Garante que a criação de um usuário padrão atribua corretamente o nível
        de acesso 'COLABORADOR' e não conceda privilégios administrativos.
        """
        user = Usuario.objects.create_user(
            username='maria.teste',
            password='123',
            first_name='Maria',
            cpf='99988877766'
        )
        
        # Validação de persistência de dados básicos
        self.assertEqual(user.first_name, 'Maria')
        
        # Verificação de regra de negócio: Perfil default deve ser COLABORADOR
        self.assertEqual(user.perfil, 'COLABORADOR')
        
        # Validação de segurança: Usuários padrão não podem ter privilégios de staff/superuser
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_criar_superusuario(self):
        """
        Garante que a criação de um superusuário atribua os privilégios totais do sistema
        e defina o perfil customizado obrigatoriamente como 'ADMIN'.
        """
        admin = Usuario.objects.create_superuser(
            username='admin.teste',
            password='123'
        )
        
        # Validação de concessão de privilégios globais (Django Admin)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        
        # Verificação de regra de negócio: Espelhamento obrigatório para o perfil ADMIN
        self.assertEqual(admin.perfil, 'ADMIN')