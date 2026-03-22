import json
import datetime
from datetime import timedelta, time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Q 
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .models import Usuario
from .forms import EditarPerfilForm, ColaboradorForm
from inventory.models import Epi, Entrega

@login_required
def dashboard(request):
    """
    Visão Geral do Sistema (BI & Analytics).
    Diferencia a interface entre a visão operacional (Colaborador) 
    e a visão gerencial (SST, Almoxarife e Admin).
    """
    user = request.user
    hoje_local = timezone.localtime(timezone.now()).date()
    
    # ---------------------------------------------------------
    # INTERFACE DO COLABORADOR (Self-Service)
    # ---------------------------------------------------------
    if user.perfil == 'COLABORADOR':
        entregas_base = Entrega.objects.filter(colaborador=user)
        atividades_recentes = entregas_base.select_related('epi').order_by('-data_entrega')[:5]
        
        context = {
            'meus_epis_ativos': entregas_base.filter(status='EM_USO').count(),
            'historico_total': entregas_base.count(),
            'atividades_recentes': atividades_recentes,
            'is_colaborador': True,
        }
        return render(request, 'dashboard/dashboard.html', context)

    # ---------------------------------------------------------
    # INTERFACE GERENCIAL (SST / ALMOXARIFADO / ADMIN)
    # ---------------------------------------------------------
    inicio_dia = timezone.make_aware(datetime.datetime.combine(hoje_local, time.min))
    fim_dia = timezone.make_aware(datetime.datetime.combine(hoje_local, time.max))

    # Indicadores de Performance (KPIs)
    pendencias_count = Entrega.objects.filter(status='EM_USO').count()
    emprestimos_hoje = Entrega.objects.filter(data_entrega__range=(inicio_dia, fim_dia)).count()
    
    # Alertas de Compliance (CA Vencido e NR-7/ASO)
    cas_vencidos = Epi.objects.filter(ca_validade__lt=hoje_local, ativo=True).count()
    aso_vencidos = Usuario.objects.filter(data_vencimento_aso__lt=hoje_local, is_active=True)

    # Análise Preditiva de Troca de EPI (Vida Útil)
    entregas_em_uso = Entrega.objects.filter(status='EM_USO').select_related('epi', 'colaborador')
    epis_vencendo_vida_util = []

    for entrega in entregas_em_uso:
        if entrega.epi.vida_util_dias > 0:
            data_vencimento_epi = entrega.data_entrega.date() + timedelta(days=entrega.epi.vida_util_dias)
            
            # Alerta com margem de 5 dias para planejamento de reposição
            if data_vencimento_epi <= hoje_local + timedelta(days=5):
                epis_vencendo_vida_util.append({
                    'colaborador': entrega.colaborador.get_full_name(),
                    'epi': entrega.epi.nome,
                    'data_entrega': entrega.data_entrega.date(),
                    'data_vencimento': data_vencimento_epi
                })

    atividades_recentes = Entrega.objects.all().select_related('colaborador', 'epi').order_by('-data_entrega')[:5]

    # Processamento de Dados para Gráficos (Chart.js)
    status_dados = [
        Entrega.objects.filter(status='EM_USO').count(),
        Entrega.objects.filter(status='DEVOLVIDO').count(),
        Entrega.objects.filter(status__in=['DESCARTADO', 'PERDIDO']).count(),
    ]

    top_entregas = Entrega.objects.values('epi__nome').annotate(total=Count('epi')).order_by('-total')[:5]
    top_epis_nomes = [item['epi__nome'] for item in top_entregas]
    top_epis_qtds = [item['total'] for item in top_entregas]

    # Histórico Semanal de Movimentação
    dias_labels = []
    entregas_por_dia = []
    for i in range(6, -1, -1):
        dia_alvo = hoje_local - timedelta(days=i)
        dias_labels.append(dia_alvo.strftime('%d/%m'))
        inicio_alvo = timezone.make_aware(datetime.datetime.combine(dia_alvo, time.min))
        fim_alvo = timezone.make_aware(datetime.datetime.combine(dia_alvo, time.max))
        qtd = Entrega.objects.filter(data_entrega__range=(inicio_alvo, fim_alvo)).count()
        entregas_por_dia.append(qtd)

    cas_vencidos_list = Epi.objects.filter(ca_validade__lt=hoje_local, ativo=True)

    context = {
        'pendencias_count': pendencias_count,
        'emprestimos_hoje': emprestimos_hoje,
        'cas_vencidos': cas_vencidos,
        'cas_vencidos_list': cas_vencidos_list,
        'aso_vencidos': aso_vencidos, 
        'epis_vencendo_vida_util': epis_vencendo_vida_util,
        'atividades_recentes': atividades_recentes,
        'grafico_status_dados': json.dumps(status_dados),
        'top_epis_nomes': json.dumps(top_epis_nomes),
        'top_epis_qtds': json.dumps(top_epis_qtds),
        'dias_labels': json.dumps(dias_labels),
        'entregas_por_dia': json.dumps(entregas_por_dia),
        'is_colaborador': False,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def editar_perfil(request):
    """Permite ao usuário autenticado gerenciar suas informações básicas de perfil."""
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('dashboard') 
    else:
        form = EditarPerfilForm(instance=request.user)
    return render(request, 'accounts/editar_perfil.html', {'form': form})

@login_required
def listar_colaboradores(request):
    """Listagem geral de colaboradores com suporte a filtros de busca."""
    if request.user.perfil == 'COLABORADOR':
        raise PermissionDenied

    query = request.GET.get('q', '')
    if query:
        colaboradores = Usuario.objects.filter(
            Q(first_name__icontains=query) | Q(cpf__icontains=query) | Q(matricula__icontains=query)
        ).distinct()
    else:
        colaboradores = Usuario.objects.all().order_by('first_name')
    return render(request, 'accounts/colaboradores_list.html', {'colaboradores': colaboradores, 'query': query})

@login_required
def cadastrar_colaborador(request):
    """
    Fluxo de cadastro de novos usuários. 
    Define automaticamente o CPF como senha inicial para o primeiro acesso.
    """
    if request.user.perfil not in ['ADMIN', 'SST']:
        raise PermissionDenied

    if request.method == 'POST':
        form = ColaboradorForm(request.POST, request.FILES, logged_user=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['cpf'])
            user.save()
            messages.success(request, f"Colaborador {user.first_name} cadastrado com sucesso!")
            return redirect('listar_colaboradores')
    else:
        form = ColaboradorForm(logged_user=request.user)
    return render(request, 'accounts/colaborador_form.html', {'form': form, 'acao': 'Cadastrar'})

@login_required
def editar_colaborador(request, id):
    """
    Edição de dados de colaboradores. 
    Inclui validação de segurança RBAC para restringir edições por hierarquia.
    """
    if request.user.perfil not in ['ADMIN', 'SST']:
        raise PermissionDenied
        
    colaborador = get_object_or_404(Usuario, id=id)
    
    # Validação de Hierarquia: Usuários SST podem editar apenas perfis de nível Colaborador.
    if request.user.perfil == 'SST' and colaborador.perfil != 'COLABORADOR':
        raise PermissionDenied
        
    if request.method == 'POST':
        form = ColaboradorForm(request.POST, request.FILES, instance=colaborador, logged_user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Dados de {colaborador.first_name} atualizados!')
            return redirect('listar_colaboradores')
    else:
        form = ColaboradorForm(instance=colaborador, logged_user=request.user)
    return render(request, 'accounts/colaborador_form.html', {'form': form, 'acao': 'Editar'})

@login_required
def deletar_colaborador(request, id):
    """Remoção de registros de usuários do sistema (Exclusão Lógica/Física)."""
    if request.user.perfil not in ['ADMIN', 'SST']:
        raise PermissionDenied
        
    colaborador = get_object_or_404(Usuario, id=id)
    
    # Validação de Hierarquia: Restringe a deleção apenas a perfis operacionais.
    if request.user.perfil == 'SST' and colaborador.perfil != 'COLABORADOR':
        raise PermissionDenied
        
    if request.method == 'POST':
        colaborador.delete()
        messages.success(request, 'Registro removido do sistema.')
        return redirect('listar_colaboradores')
    return render(request, 'accounts/colaborador_confirm_delete.html', {'colaborador': colaborador})

def custom_403(request, exception=None):
    """Handler customizado para violações de permissão (HTTP 403 Forbidden)."""
    return render(request, '403.html', status=403)