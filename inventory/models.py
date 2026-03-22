from django.db import models
from django.conf import settings 
from django.core.exceptions import ValidationError
from django.utils import timezone

class Epi(models.Model):
    """
    Representa o catálogo de Equipamentos de Proteção Individual (EPI).
    Armazena dados técnicos, certificações de aprovação (CA) e 
    parâmetros de ciclo de vida para fins de conformidade com a NR-6.
    """
    # Dados de Identificação e Classificação
    codigo = models.CharField('Código do EPI', max_length=50, unique=True)
    nome = models.CharField('Nome', max_length=200)
    categoria = models.CharField('Categoria', max_length=100, blank=True, null=True)
    tamanho = models.CharField('Tamanho', max_length=20, blank=True, null=True)
    
    # Certificações e Validades Jurídicas (SST)
    ca_numero = models.CharField('Número do CA', max_length=30, blank=True, null=True)
    ca_validade = models.DateField('Validade do CA', blank=True, null=True)
    
    # Parâmetros de Ciclo de Vida Operacional
    vida_util_dias = models.PositiveIntegerField(
        'Vida Útil (Dias)', 
        default=0, 
        help_text="Estimativa de durabilidade para fins de troca preventiva."
    )
    
    # Gestão de Disponibilidade
    estoque = models.PositiveIntegerField('Quantidade em Estoque', default=0)
    ativo = models.BooleanField('Ativo no Sistema', default=True)
    
    # Metadados de Auditoria
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.codigo} - {self.nome} (Estoque: {self.estoque})"
    
class Entrega(models.Model):
    """
    Registra o fluxo de custódia de EPIs entre a empresa e o colaborador.
    Gerencia estados de uso, devoluções e validações rigorosas de segurança 
    do trabalho e controle de estoque.
    """
    STATUS_CHOICES = (
        ('EM_USO', 'Em Uso (Com o funcionário)'),
        ('DEVOLVIDO', 'Devolvido (Voltou pro estoque)'),
        ('DESCARTADO', 'Descartado / Danificado'),
        ('PERDIDO', 'Perdido'),
    )

    # Relacionamentos de Custódia
    colaborador = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='epis_recebidos',
        verbose_name='Colaborador (Beneficiário)'
    )
    
    epi = models.ForeignKey(
        Epi, 
        on_delete=models.RESTRICT, 
        related_name='entregas',
        verbose_name='Equipamento (EPI)'
    )
    
    quantidade = models.PositiveIntegerField('Quantidade Movimentada', default=1)
    
    # Controle Temporal e de Status
    status = models.CharField('Status da Entrega', max_length=20, choices=STATUS_CHOICES, default='EM_USO')
    data_entrega = models.DateTimeField('Data da Entrega', auto_now_add=True)
    data_devolucao = models.DateTimeField('Data da Devolução/Encerramento', blank=True, null=True)
    
    observacao = models.TextField('Observações de Campo', blank=True, null=True)

    def __str__(self):
        return f"{self.quantidade}x {self.epi.nome} -> {self.colaborador.first_name} ({self.get_status_display()})"

    def clean(self):
        """
        Executa a validação lógica e de conformidade antes da persistência no banco de dados.
        Implementa travas de segurança baseadas em normas regulamentadoras e disponibilidade de inventário.
        """
        hoje = timezone.now().date()

        # Validação 1: Verificação de Disponibilidade Física
        if not self.pk and self.epi.estoque < self.quantidade:
            raise ValidationError({'quantidade': f'Estoque insuficiente. Saldo atual: {self.epi.estoque}.'})
            
        # Validação 2: Consistência de Datas no Encerramento de Custódia
        if self.status in ['DEVOLVIDO', 'DESCARTADO', 'PERDIDO'] and not self.data_devolucao:
            self.data_devolucao = timezone.now()

        # Validação 3: Compliance NR-6 (Certificado de Aprovação Vencido)
        if self.epi_id and self.epi.ca_validade:
            if self.epi.ca_validade < hoje:
                data_formatada = self.epi.ca_validade.strftime("%d/%m/%Y")
                raise ValidationError(f'Bloqueio de Compliance (NR-6): O CA deste EPI venceu em {data_formatada}.')

        # Validação 4: Compliance NR-7 (Saúde Ocupacional/ASO)
        if not self.pk and self.colaborador_id:
            if self.colaborador.data_vencimento_aso and self.colaborador.data_vencimento_aso < hoje:
                data_vencimento = self.colaborador.data_vencimento_aso.strftime("%d/%m/%Y")
                raise ValidationError({
                    'colaborador': f'Bloqueio de Segurança (NR-7): ASO do colaborador expirou em {data_vencimento}.'
                })

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método de salvamento para gerenciar a atualização atômica do inventário.
        Sincroniza automaticamente o saldo do estoque com base nas movimentações de entrega e devolução.
        """
        is_new = self.pk is None

        if is_new:
            # Fluxo de Saída: Deduz do estoque físico no momento da entrega
            self.epi.estoque -= self.quantidade
            self.epi.save()
        else:
            # Fluxo de Retorno: Reintegra ao estoque apenas em caso de devolução bem-sucedida
            entrega_antiga = Entrega.objects.get(pk=self.pk)
            
            if entrega_antiga.status == 'EM_USO' and self.status == 'DEVOLVIDO':
                self.epi.estoque += self.quantidade
                self.epi.save()

        super().save(*args, **kwargs)