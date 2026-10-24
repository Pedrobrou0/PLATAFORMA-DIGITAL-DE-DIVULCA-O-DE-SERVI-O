from django import forms
from .models import Categoria, Servico


class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria

        fields = [
            'nome',
            'profissionais'
        ]


class ServicoForm(forms.ModelForm):

    class Meta:
        model = Servico

        fields = [
            'categoria',
            'titulo',
            'descricao',
            'preco',
            'imagem'
        ]