from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.db import models
from django.core.exceptions import ValidationError, PermissionDenied
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

from .models import Epi, Entrega
from .forms import EpiForm, EntregaForm
from accounts.models import Usuario

@login_required
def lista_inventory(request):
    """
    Lista o catálogo de EPIs disponíveis. 
    Acesso liberado para todos os níveis de perfil para consulta de CA e estoque.
    """
    hoje = timezone.now().date()
    busca = request.GET.get('search')
    epis = Epi.objects.all().order_by('nome')
    
    if busca:
        epis = epis.filter(nome__icontains=busca)
    
    return render(request, 'inventory/lista_epis.html', {'epis': epis, 'hoje': hoje})

@login_required
def criar_epi(request):
    """Permite o registro de novos equipamentos por perfis administrativos e operacionais de estoque."""
    if request.user.perfil not in ['ADMIN', 'SST', 'ALMOXARIFE']:
        raise PermissionDenied

    if request.method == 'POST':
        form = EpiForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Equipamento catalogado com sucesso.")
            return redirect('lista_epis')
    else:
        form = EpiForm()
    return render(request, 'inventory/form_epi.html', {'form': form, 'titulo': 'Cadastrar Novo EPI'})

@login_required
def editar_epi(request, pk):
    """Atualização de dados técnicos, CA e níveis de inventário."""
    if request.user.perfil not in ['ADMIN', 'SST', 'ALMOXARIFE']:
        raise PermissionDenied
    
    epi = get_object_or_404(Epi, pk=pk)
    if request.method == 'POST':
        form = EpiForm(request.POST, instance=epi)
        if form.is_valid():
            form.save()
            messages.success(request, f"Registro de '{epi.nome}' atualizado.")
            return redirect('lista_epis')
    else:
        form = EpiForm(instance=epi)
    return render(request, 'inventory/form_epi.html', {'form': form, 'titulo': 'Editar EPI'})

@login_required
def excluir_epi(request, pk):
    """Remoção definitiva do item. Restrito ao perfil de Administrador com dupla confirmação."""
    if request.user.perfil != 'ADMIN':
        raise PermissionDenied
    
    epi = get_object_or_404(Epi, pk=pk)
    if request.method == 'POST':
        confirmacao = request.POST.get('confirmacao_nome')
        if confirmacao == epi.nome:
            epi.delete()
            messages.success(request, "Registro removido do inventário.")
            return redirect('lista_epis')
        messages.error(request, "Falha na confirmação: Nome do EPI não coincide.")
    return render(request, 'inventory/confirmar_exclusao.html', {'epi': epi})

@login_required
def lista_entregas(request):
    """
    Exibe o histórico de movimentações. 
    Colaboradores possuem visão restrita aos seus próprios registros (Self-access).
    """
    if request.user.perfil == 'COLABORADOR':
        entregas = Entrega.objects.filter(colaborador=request.user).select_related('epi').order_by('-data_entrega')
    else:
        entregas = Entrega.objects.all().select_related('colaborador', 'epi').order_by('-data_entrega')
    
    busca = request.GET.get('q')
    if busca and request.user.perfil != 'COLABORADOR':
        entregas = entregas.filter(
            models.Q(colaborador__first_name__icontains=busca) | 
            models.Q(epi__nome__icontains=busca)
        )
    return render(request, 'inventory/lista_entregas.html', {'entregas': entregas})

@login_required
def registrar_entrega(request):
    """Inicia o fluxo de custódia de um EPI, aplicando validações de perfil e disponibilidade."""
    if request.user.perfil not in ['ADMIN', 'ALMOXARIFE', 'COLABORADOR', 'SST']:
        raise PermissionDenied

    if request.method == 'POST':
        form = EntregaForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                entrega = form.save(commit=False)
                if request.user.perfil == 'COLABORADOR':
                    entrega.colaborador = request.user
                
                entrega.save()
                messages.success(request, "Movimentação de saída registrada com sucesso.")
                return redirect('lista_entregas')
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = EntregaForm(user=request.user)
    
    return render(request, 'inventory/form_entrega.html', {'form': form})

@login_required
def registrar_devolucao(request, pk):
    """Finaliza ou altera o estado de custódia do equipamento (Devolução, Perda ou Descarte)."""
    entrega = get_object_or_404(Entrega, pk=pk)
    
    # Validação de Propriedade: Garante que colaboradores não encerrem registros de terceiros.
    if request.user.perfil == 'COLABORADOR' and entrega.colaborador != request.user:
        messages.error(request, "Violação de acesso: Você não possui permissão para este registro.")
        return redirect('lista_entregas')
    
    if request.user.perfil not in ['ADMIN', 'ALMOXARIFE', 'COLABORADOR', 'SST']:
        raise PermissionDenied
    
    if request.method == 'POST':
        novo_status = request.POST.get('novo_status')

        if novo_status in ['DEVOLVIDO', 'DESCARTADO', 'PERDIDO']:
            if entrega.status == 'EM_USO':
                entrega.status = novo_status
                entrega.data_devolucao = timezone.now()
                entrega.save()
                
                # Feedback contextual baseado na natureza da baixa
                if novo_status == 'DEVOLVIDO':
                    messages.success(request, f"Item {entrega.epi.nome} reintegrado ao estoque físico.")
                else:
                    messages.warning(request, f"Baixa registrada como {novo_status}. O saldo não foi recomposto.")
            else:
                messages.warning(request, "Este registro já possui baixa confirmada.")
        else:
            messages.error(request, "Parâmetro de status inválido.")
            
    return redirect('lista_entregas')

@login_required
def busca_geral(request):
    """Interface de busca global para rápida localização de ativos e beneficiários."""
    if request.user.perfil == 'COLABORADOR':
        raise PermissionDenied
        
    query = request.GET.get('q', '')
    epis = Epi.objects.filter(models.Q(nome__icontains=query) | models.Q(codigo__icontains=query)) if query else []
    colaboradores = Usuario.objects.filter(models.Q(first_name__icontains=query) | models.Q(cpf__icontains=query)) if query else []
    
    return render(request, 'inventory/busca_geral.html', {'query': query, 'epis': epis, 'colaboradores': colaboradores})

# -----------------------------------------------------------------------------
# SUBSISTEMA DE GERAÇÃO DE DOCUMENTOS (PDF ENGINE)
# -----------------------------------------------------------------------------

def render_to_pdf(template_src, context_dict={}):
    """Motor de renderização HTML para PDF via pisa (xhtml2pdf)."""
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="documento_epi.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro crítico na geração do documento PDF.', status=500)
    return response

@login_required
def gerar_recibo_pdf(request, pk):
    """Emite comprovante individual de entrega para assinatura e arquivo."""
    entrega = get_object_or_404(Entrega, pk=pk)
    
    if request.user.perfil == 'COLABORADOR' and entrega.colaborador != request.user:
        raise PermissionDenied
        
    context = {'entrega': entrega, 'hoje': timezone.now()}
    return render_to_pdf('inventory/pdf_recibo.html', context)

@login_required
def gerar_ficha_nr6_pdf(request, usuario_id):
    """Emite a Ficha de Controle de EPI (NR-6) consolidada do colaborador."""
    colaborador = get_object_or_404(Usuario, pk=usuario_id)
    
    if request.user.perfil == 'COLABORADOR' and colaborador != request.user:
        raise PermissionDenied

    entregas = Entrega.objects.filter(colaborador=colaborador).order_by('data_entrega')
    
    context = {
        'colaborador': colaborador,
        'entregas': entregas,
        'hoje': timezone.now()
    }
    return render_to_pdf('inventory/pdf_ficha_nr6.html', context)