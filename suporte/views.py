from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from .models import Feedback, Avaliacao
from .forms import FeedbackForm, FeedbackEditarForm, AvaliacaoForm


d@login_required
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
        form.save()

        return redirect('lista_feedbacks')

    return render(request, 'suporte/feedback_form.html', {
        'form': form
    })


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
        'avaliacao': avaliacao
    })

def criar_avaliacao(request):
    form = AvaliacaoForm(request.POST or None)

    if form.is_valid():
        form.save()

        return redirect('lista_avaliacoes')

    return render(request, 'suporte/avaliacao_form.html', {
        'form': form
    })


def editar_avaliacao(request, id):
    avaliacao = Avaliacao.objects.get(id=id)

    form = AvaliacaoForm(
        request.POST or None,
        instance=avaliacao
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
        avaliacao.delete()

        return redirect('lista_avaliacoes')

    return render(request, 'suporte/confirmar_delete.html', {
        'objeto': avaliacao,
        'lista_url': 'lista_avaliacoes'
    })