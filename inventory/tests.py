from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse

from accounts.models import Usuario
from inventory.models import Epi, Entrega
from inventory.forms import EpiForm

class RegrasDeNegocioTestCase(TestCase):
    """
    Suíte de testes para validação das regras de negócio do inventário.
    Cobre integridade de estoque, compliance com NR-6 (CA) e NR-7 (ASO).
    """
    
    def setUp(self):
        """Prepara o ambiente de teste com massa de dados sanitizada."""
        self.hoje = timezone.now().date()
        self.ontem = self.hoje - timedelta(days=1)
        self.amanha = self.hoje + timedelta(days=1)

        # Cadastro de colaborador em conformidade com saúde ocupacional
        self.colaborador = Usuario.objects.create(
            username='joao.teste',
            first_name='João',
            cpf='11122233344',
            data_vencimento_aso=self.amanha
        )

        # Cadastro de equipamento com estoque inicial e validade ativa
        self.epi = Epi.objects.create(
            codigo='TESTE-01',
            nome='Bota de Segurança',
            estoque=10,
            ca_validade=self.amanha,
            vida_util_dias=180
        )

    def test_sincronizacao_estoque_na_entrega(self):
        """Verifica se o método save() realiza a dedução atômica no inventário."""
        Entrega.objects.create(
            colaborador=self.colaborador, 
            epi=self.epi, 
            quantidade=2
        )
        self.epi.refresh_from_db()
        self.assertEqual(self.epi.estoque, 8)

    def test_validacao_compliance_nr6_ca_vencido(self):
        """Garante que o sistema bloqueie a entrega de EPIs com Certificado de Aprovação (CA) expirado."""
        self.epi.ca_validade = self.ontem
        self.epi.save()

        entrega = Entrega(colaborador=self.colaborador, epi=self.epi, quantidade=1)
        
        with self.assertRaises(ValidationError) as erro:
            entrega.clean()
            
        self.assertIn("Bloqueio de Compliance (NR-6)", str(erro.exception))

    def test_validacao_compliance_nr7_aso_vencido(self):
        """Verifica o bloqueio de movimentação para colaboradores com exame médico (ASO) vencido."""
        self.colaborador.data_vencimento_aso = self.ontem
        self.colaborador.save()

        entrega = Entrega(colaborador=self.colaborador, epi=self.epi, quantidade=1)
        
        with self.assertRaises(ValidationError) as erro:
            entrega.clean()
            
        self.assertIn("Bloqueio de Segurança (NR-7)", str(erro.exception))

    def test_reintegracao_estoque_na_devolucao(self):
        """Verifica se a devolução do equipamento recompõe corretamente o saldo do inventário."""
        entrega = Entrega.objects.create(
            colaborador=self.colaborador, 
            epi=self.epi, 
            quantidade=2,
            status='EM_USO'
        )
        
        entrega.status = 'DEVOLVIDO'
        entrega.save()
        
        self.epi.refresh_from_db()
        self.assertEqual(self.epi.estoque, 10)

    def test_manutencao_estoque_em_caso_de_descarte(self):
        """Garante que baixas por descarte ou perda não reintegrem itens ao estoque físico."""
        entrega = Entrega.objects.create(
            colaborador=self.colaborador, 
            epi=self.epi, 
            quantidade=3
        )
        
        entrega.status = 'DESCARTADO'
        entrega.save()
        
        self.epi.refresh_from_db()
        self.assertEqual(self.epi.estoque, 7)

class ViewsSegurancaTestCase(TestCase):
    """Validação de controle de acesso (RBAC) e proteção de endpoints."""
    
    def setUp(self):
        self.colaborador = Usuario.objects.create_user(
            username='operacional', password='123', perfil='COLABORADOR', 
            cpf='11111111111', matricula='1001'
        )
        self.admin = Usuario.objects.create_superuser(
            username='gestor', password='123', 
            cpf='22222222222', matricula='1002'
        )

    def test_restricao_acesso_perfil_operacional(self):
        """Verifica se usuários de nível 'COLABORADOR' possuem acesso negado a funções administrativas."""
        self.client.force_login(self.colaborador)
        response = self.client.get(reverse('criar_epi'))
        self.assertNotEqual(response.status_code, 200)

    def test_permissao_acesso_perfil_administrativo(self):
        """Garante que usuários 'ADMIN' acessem normalmente as funcionalidades de gestão de estoque."""
        self.client.force_login(self.admin)
        response = self.client.get(reverse('criar_epi'))
        self.assertEqual(response.status_code, 200)

class EpiFormTestCase(TestCase):
    """Testes de integridade e validação de entrada de dados nos formulários."""
    
    def test_validacao_tipo_dado_estoque(self):
        """Verifica se o formulário rejeita entradas não numéricas em campos de saldo de estoque."""
        dados_do_form = {
            'codigo': 'TEST-99',
            'nome': 'Capacete',
            'estoque': 'INVALIDO',
            'vida_util_dias': 30,
            'ca_validade': '2030-01-01' 
        }
        form = EpiForm(data=dados_do_form)
        self.assertFalse(form.is_valid())
        self.assertIn('estoque', form.errors)

    def test_persistência_dados_validos(self):
        """Valida o processamento bem-sucedido (Happy Path) de dados íntegros no formulário."""
        amanha = timezone.now().date() + timedelta(days=1)
        dados_do_form = {
            'codigo': 'TEST-100',
            'nome': 'Capacete MSA',
            'estoque': 10,
            'vida_util_dias': 30,
            'ca_validade': amanha
        }
        form = EpiForm(data=dados_do_form)
        self.assertTrue(form.is_valid())