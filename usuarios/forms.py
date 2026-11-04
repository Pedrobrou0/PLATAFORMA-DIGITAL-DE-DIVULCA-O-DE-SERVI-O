from django import forms
from django.core.files.uploadedfile import UploadedFile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from servicos.models import Categoria
from .models import Perfil, Profissional


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

TAMANHO_MAXIMO_IMAGEM = 5 * 1024 * 1024  # 5 MB (RF011)


def validar_tamanho_imagem(arquivo):
    # Só confere arquivo novo; a imagem que já estava salva não é reenviada.
    if isinstance(arquivo, UploadedFile) and arquivo.size > TAMANHO_MAXIMO_IMAGEM:
        raise forms.ValidationError('A imagem pode ter no máximo 5 MB.')

    return arquivo


class PerfilForm(forms.ModelForm):

    class Meta:
        model = Perfil

        fields = [
            'foto',
            'banner',
            'cor_tema',
            'bio',
            'instagram'
        ]

        labels = {
            'foto': 'Foto de perfil',
            'banner': 'Imagem de capa (banner)',
            'cor_tema': 'Cor do perfil',
            'bio': 'Frase de apresentação',
            'instagram': 'Instagram',
        }

        help_texts = {
            'foto': 'JPG ou PNG, até 5 MB. Fica melhor uma imagem quadrada.',
            'banner': 'JPG ou PNG, até 5 MB. Fica melhor uma imagem larga, como 1200 × 300.',
            'cor_tema': 'Usada no topo do perfil quando não há imagem de capa.',
            'bio': 'Até 160 caracteres. Aparece embaixo do seu nome.',
            'instagram': 'Só o nome de usuário, sem o @.',
        }

        widgets = {
            'bio': forms.Textarea(attrs={'rows': 2, 'maxlength': 160}),
        }

    def clean_foto(self):
        return validar_tamanho_imagem(self.cleaned_data.get('foto'))

    def clean_banner(self):
        return validar_tamanho_imagem(self.cleaned_data.get('banner'))

    def clean_instagram(self):
        instagram = self.cleaned_data.get('instagram', '')

        # Aceita "@usuario" ou o link inteiro e guarda só o nome.
        instagram = instagram.strip().rstrip('/').split('/')[-1]

        return instagram.lstrip('@')
