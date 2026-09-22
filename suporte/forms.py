from django import forms
from .models import Feedback, Avaliacao


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback

        fields = [
            'usuario',
            'tipo',
            'mensagem',
            'status'
        ]


class AvaliacaoForm(forms.ModelForm):

    class Meta:
        model = Avaliacao

        fields = [
            'cliente',
            'profissional',
            'nota',
            'comentario',
            'tipo_autor'
        ]