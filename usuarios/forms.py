from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from servicos.models import Categoria
from .models import Profissional


class ClienteCadastroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Usado para redefinir a senha.'
    )

    class Meta(UserCreationForm.Meta):
        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email'
        ]


class ProfissionalCadastroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Usado para redefinir a senha.'
    )

    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = Profissional

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'telefone',
            'cidade',
            'descricao',
            'foto',
            'categorias'
        ]

    def save(self, commit=True):
        profissional = super().save(commit=commit)

        if commit:
            profissional.categorias.set(
                self.cleaned_data['categorias']
            )

        return profissional


class ProfissionalForm(forms.ModelForm):
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        required=True
    )

    class Meta:
        model = Profissional
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'telefone',
            'cidade',
            'descricao',
            'foto',
            'categorias'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['categorias'].initial = (
                self.instance.categorias.all()
            )

    def save(self, commit=True):
        profissional = super().save(commit=False)

        if commit:
            profissional.save()

            profissional.categorias.set(
                self.cleaned_data['categorias']
            )

        return profissional