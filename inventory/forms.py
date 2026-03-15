from django import forms
from .models import Epi, Entrega

class EpiForm(forms.ModelForm):
    """
    Formulário para gestão do catálogo de Equipamentos de Proteção Individual.
    Inclui parâmetros de controle de estoque, validade jurídica (CA) 
    e ciclo de vida operacional (Vida Útil).
    """
    class Meta:
        model = Epi
        fields = [
            'codigo', 'nome', 'categoria', 'tamanho', 'ca_numero', 
            'ca_validade', 'vida_util_dias', 'estoque', 'ativo'
        ]
        
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: EPI-001'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Bota de Segurança'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Calçados'}),
            'tamanho': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 40, M, Único'}),
            'ca_numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 12345'}),
            'ca_validade': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'vida_util_dias': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 180', 'min': '0'}),
            'estoque': forms.NumberInput(attrs={'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }

class EntregaForm(forms.ModelForm):
    """
    Formulário para registro de movimentação e custódia de EPIs.
    Implementa validações de contexto para garantir que colaboradores 
    não alterem o destino da solicitação.
    """
    class Meta:
        model = Entrega
        fields = ['colaborador', 'epi', 'quantidade', 'observacao']
        
        widgets = {
            'colaborador': forms.Select(attrs={'class': 'form-control'}),
            'epi': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observações de entrega ou estado do equipamento...'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Sobrescreve a inicialização para aplicar regras de negócio baseadas no perfil.
        Em casos de auto-solicitação (Colaborador), o campo de destino é 
        travado para garantir a integridade da operação.
        """
        user = kwargs.pop('user', None)
        super(EntregaForm, self).__init__(*args, **kwargs)
        
        # Lógica de Restrição de Perfil (Self-Service Security)
        if user and user.perfil == 'COLABORADOR':
            self.fields['colaborador'].queryset = user.__class__.objects.filter(id=user.id)
            self.fields['colaborador'].initial = user
            
            # Bloqueio de interface para evitar manipulação de dados
            self.fields['colaborador'].widget.attrs['readonly'] = True
            self.fields['colaborador'].widget.attrs['style'] = 'pointer-events: none; background-color: #e9ecef;'