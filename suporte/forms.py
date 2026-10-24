from django import forms
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