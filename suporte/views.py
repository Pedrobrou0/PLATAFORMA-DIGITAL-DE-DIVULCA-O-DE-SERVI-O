from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from .models import Feedback, Avaliacao, TipoAutorAvaliacao
from .forms import (
    FeedbackForm,
    FeedbackEditarForm,
    AvaliacaoClienteForm,
    AvaliacaoProfissionalForm,
)
from usuarios.permissoes import eh_profissional


def eh_autor(usuario, avaliacao):
    if avaliacao.tipo_autor == TipoAutorAvaliacao.PROFISSIONAL:
        return avaliacao.profissional_id == usuario.id

    return avaliacao.cliente_id == usuario.id


@login_required
def lista_feedbacks(request):
    if request.user.has_perm('suporte.view_feedback'):
        # Gerenciar Feedbacks (Administrador)
        feedbacks = Feedback.objects.all()
    else:
        feedbacks = Feedback.objects.filter(usuario=request.user)

    return render(request, 'suporte/feedback_lista.html', {
        'feedbacks': feedbacks.order_by('-data_envio')
    })


@login_required
def detalhe_feedback(request, id):
    feedback = Feedback.objects.get(id=id)

    if (
        feedback.usuario_id != request.user.id
        and not request.user.has_perm('suporte.view_feedback')
    ):
        raise PermissionDenied

    return render(request, 'suporte/feedback_detalhe.html', {
        'feedback': feedback
    })

@login_required
@permission_required('suporte.add_feedback', raise_exception=True)
def criar_feedback(request):
    form = FeedbackForm(request.POST or None)

    if form.is_valid():
        feedback = form.save(commit=False)
        feedback.usuario = request.user
        feedback.enviar()

        return redirect('detalhe_feedback', id=feedback.id)

    return render(request, 'suporte/feedback_form.html', {
        'form': form
    })


@login_required
@permission_required('suporte.change_feedback', raise_exception=True)
def editar_feedback(request, id):
    feedback = Feedback.objects.get(id=id)

    form = FeedbackEditarForm(
        request.POST or None,
        instance=feedback
    )

    if form.is_valid():
        feedback.alterar_status(form.cleaned_data['status'])

        return redirect('detalhe_feedback', id=feedback.id)

    return render(request, 'suporte/feedback_form.html', {
        'form': form
    })


@login_required
@permission_required('suporte.delete_feedback', raise_exception=True)
def deletar_feedback(request, id):
    feedback = Feedback.objects.get(id=id)

    if request.method == 'POST':
        feedback.delete()

        return redirect('lista_feedbacks')

    return render(request, 'suporte/confirmar_delete.html', {
        'objeto': feedback,
        'lista_url': 'lista_feedbacks'
    })

def lista_avaliacoes(request):
    avaliacoes = Avaliacao.objects.all()

    return render(request, 'suporte/avaliacao_lista.html', {
        'avaliacoes': avaliacoes
    })


def detalhe_avaliacao(request, id):
    avaliacao = Avaliacao.objects.get(id=id)

    return render(request, 'suporte/avaliacao_detalhe.html', {
        'avaliacao': avaliacao,
        'eh_autor': eh_autor(request.user, avaliacao)
    })

@login_required
@permission_required('suporte.add_avaliacao', raise_exception=True)
def criar_avaliacao(request):
    if eh_profissional(request.user):
        form = AvaliacaoProfissionalForm(
            request.POST or None,
            usuario=request.user,
            initial={'cliente': request.GET.get('cliente')}
        )
    else:
        form = AvaliacaoClienteForm(
            request.POST or None,
            usuario=request.user,
            initial={'profissional': request.GET.get('profissional')}
        )

    if form.is_valid():
        avaliacao = form.save(commit=False)

        # O autor é sempre quem está logado.
        if eh_profissional(request.user):
            avaliacao.profissional = request.user.profissional
            avaliacao.tipo_autor = TipoAutorAvaliacao.PROFISSIONAL
        else:
            avaliacao.cliente = request.user
            avaliacao.tipo_autor = TipoAutorAvaliacao.CLIENTE

        avaliacao.avaliar()

        return redirect('detalhe_avaliacao', id=avaliacao.id)

    return render(request, 'suporte/avaliacao_form.html', {
        'form': form
    })


@login_required
@permission_required('suporte.change_avaliacao', raise_exception=True)
def editar_avaliacao(request, id):
    avaliacao = Avaliacao.objects.get(id=id)

    if not eh_autor(request.user, avaliacao):
        raise PermissionDenied

    if avaliacao.tipo_autor == TipoAutorAvaliacao.PROFISSIONAL:
        formulario = AvaliacaoProfissionalForm
    else:
        formulario = AvaliacaoClienteForm

    form = formulario(
        request.POST or None,
        instance=avaliacao,
        usuario=request.user
    )

    if form.is_valid():
        form.save()

        return redirect('detalhe_avaliacao', id=avaliacao.id)

    return render(request, 'suporte/avaliacao_form.html', {
        'form': form
    })


@login_required
@permission_required('suporte.delete_avaliacao', raise_exception=True)
def deletar_avaliacao(request, id):
    avaliacao = Avaliacao.objects.get(id=id)

    if not (eh_autor(request.user, avaliacao) or request.user.is_superuser):
        raise PermissionDenied

    if request.method == 'POST':
        avaliacao.delete()

        return redirect('lista_avaliacoes')

    return render(request, 'suporte/confirmar_delete.html', {
        'objeto': avaliacao,
        'lista_url': 'lista_avaliacoes'
    })