from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


# Formatos aceitos nas imagens de perfil (RF011: JPG ou PNG).
FORMATOS_IMAGEM = ['jpg', 'jpeg', 'png']


class Profissional(User):
    telefone = models.CharField(max_length=20)
    cidade = models.CharField(max_length=100)
    descricao = models.TextField()

    foto = models.ImageField(
        upload_to='profissionais/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.get_full_name() or self.username


class CorTema(models.TextChoices):
    # Os valores são as cores do AdminLTE (bg-primary, bg-gradient-purple...).
    AZUL = 'primary', 'Azul'
    VERDE = 'success', 'Verde'
    CIANO = 'info', 'Ciano'
    AMARELO = 'warning', 'Amarelo'
    VERMELHO = 'danger', 'Vermelho'
    ROXO = 'purple', 'Roxo'
    ANIL = 'indigo', 'Anil'
    TURQUESA = 'teal', 'Turquesa'
    LARANJA = 'orange', 'Laranja'
    ROSA = 'pink', 'Rosa'
    MARINHO = 'navy', 'Azul-marinho'


class Perfil(models.Model):
    """Personalização do perfil de qualquer usuário (cliente, profissional ou ADM)."""

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil'
    )

    foto = models.ImageField(
        upload_to='perfis/fotos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(FORMATOS_IMAGEM)]
    )

    banner = models.ImageField(
        upload_to='perfis/banners/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(FORMATOS_IMAGEM)]
    )

    bio = models.CharField(
        max_length=160,
        blank=True
    )

    cor_tema = models.CharField(
        max_length=20,
        choices=CorTema.choices,
        default=CorTema.AZUL
    )

    instagram = models.CharField(
        max_length=30,
        blank=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    @classmethod
    def do_usuario(cls, usuario):
        """Devolve o perfil do usuário, criando um perfil padrão na primeira vez."""
        perfil, _ = cls.objects.get_or_create(usuario_id=usuario.id)
        return perfil

    def imagem_foto(self):
        """Foto do perfil; se não tiver, usa a foto do cadastro de profissional."""
        if self.foto:
            return self.foto

        profissional = Profissional.objects.filter(id=self.usuario_id).first()

        if profissional and profissional.foto:
            return profissional.foto

        return None

    def __str__(self):
        return f'Perfil de {self.usuario}'
