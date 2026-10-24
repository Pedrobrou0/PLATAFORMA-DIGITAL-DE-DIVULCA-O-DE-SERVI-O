from django import forms
from servicos.models import Servico
from .models import Solicitacao


class SolicitacaoForm(forms.ModelForm):

    class Meta:
        model = Solicitacao

        fields = [
            'servico',
            'descricao'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['servico'].queryset = (
            Servico.objects.filter(ativo=True)
        )


class SolicitacaoEditarForm(forms.ModelForm):

    class Meta:
        model = Solicitacao

        fields = [
            'servico',
            'descricao'
        ]