from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

from usuarios.models import Profissional


class TipoAutorAvaliacao(models.TextChoices):
    CLIENTE = 'CLIENTE', 'Cliente'
    PROFISSIONAL = 'PROFISSIONAL', 'Profissional'


class TipoFeedback(models.TextChoices):
    SUGESTAO = 'SUGESTAO', 'Sugestão'
    OPINIAO = 'OPINIAO', 'Opinião'
    PROBLEMA = 'PROBLEMA', 'Problema'


class StatusFeedback(models.TextChoices):
    PENDENTE = 'PENDENTE', 'Pendente'
    EM_ANALISE = 'EM_ANALISE', 'Em análise'
    RESOLVIDO = 'RESOLVIDO', 'Resolvido'


class Avaliacao(models.Model):
    cliente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='avaliacoes_cliente'
    )

    profissional = models.ForeignKey(
        Profissional,
        on_delete=models.CASCADE,
        related_name='avaliacoes_profissional'
    )

    nota = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    comentario = models.TextField()

    data_avaliacao = models.DateTimeField(
        auto_now_add=True
    )

    tipo_autor = models.CharField(
        max_length=20,
        choices=TipoAutorAvaliacao.choices
    )

    def avaliar(self):
        self.save()

    def __str__(self):
        return f'{self.cliente} - {self.profissional} - {self.nota}'


class Feedback(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )

    tipo = models.CharField(
        max_length=20,
        choices=TipoFeedback.choices
    )

    mensagem = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=StatusFeedback.choices,
        default=StatusFeedback.PENDENTE
    )

    data_envio = models.DateTimeField(
        auto_now_add=True
    )

    def enviar(self):
        self.save()

    def alterar_status(self, novo_status):
        self.status = novo_status
        self.save()

    def __str__(self):
        return f'{self.usuario} - {self.tipo}'