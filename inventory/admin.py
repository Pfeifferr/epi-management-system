from django.contrib import admin
from .models import Epi, Entrega

@admin.register(Epi)
class EpiAdmin(admin.ModelAdmin):
    """
    Configuração da interface administrativa para o catálogo de EPIs.
    Gerencia o ciclo de vida dos equipamentos, controle de estoque e validade de CAs.
    """
    # Configurações de exibição na listagem principal (Grid)
    list_display = ('codigo', 'nome', 'tamanho', 'estoque', 'ca_numero', 'ativo')
    
    # Mecanismo de busca otimizado por múltiplos identificadores
    search_fields = ('codigo', 'nome', 'ca_numero')
    
    # Filtros de segmentação para gestão de disponibilidade e categorias
    list_filter = ('ativo', 'categoria')

@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    """
    Interface administrativa para monitoramento do fluxo de entregas e devoluções.
    Focada na rastreabilidade de custódia e integridade dos registros de movimentação.
    """
    # Colunas de auditoria para acompanhamento de movimentações
    list_display = ('epi', 'colaborador', 'quantidade', 'status', 'data_entrega', 'data_devolucao')
    
    # Segmentação por status de custódia e períodos cronológicos
    list_filter = ('status', 'data_entrega')
    
    # Busca avançada via relacionamentos (Foreign Keys)
    search_fields = ('colaborador__first_name', 'colaborador__cpf', 'epi__nome')
    
    # Garantia de integridade: registros temporais não editáveis para evitar fraude
    readonly_fields = ('data_entrega',)