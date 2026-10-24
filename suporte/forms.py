from django import forms
from django.contrib.auth.models import User

from interacoes.models import StatusSolicitacao
from usuarios.models import Profissional
from .models import Feedback, Avaliacao


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback

        fields = [

            'tipo',
            'mensagem'
        ]


class FeedbackEditarForm(forms.ModelForm):
    # Gerenciar Feedbacks: o Administrador só altera o status.

    class Meta:
        model = Feedback

        fields = [

            'status'
        ]


class AvaliacaoClienteForm(forms.ModelForm):
    # O cliente avalia um profissional que concluiu um serviço para ele.

    class Meta:
        model = Avaliacao

        fields = [
            'profissional',
            'nota',
            'comentario'
        ]

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['profissional'].queryset = Profissional.objects.filter(
            servicos__solicitacoes__cliente=usuario,
            servicos__solicitacoes__status=StatusSolicitacao.CONCLUIDA
        ).distinct()


class AvaliacaoProfissionalForm(forms.ModelForm):
    # O profissional avalia um cliente que ele já atendeu.

    class Meta:
        model = Avaliacao

        fields = [
            'cliente',
            'nota',
            'comentario'
        ]

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['cliente'].queryset = User.objects.filter(
            solicitacoes__servico__profissional_id=usuario.id,
            solicitacoes__status=StatusSolicitacao.CONCLUIDA
        ).distinct()