from django.shortcuts import render, redirect
from .models import Feedback, Avaliacao
from .forms import FeedbackForm, AvaliacaoForm


def lista_feedbacks(request):
    feedbacks = Feedback.objects.all()

    return render(request, 'suporte/feedback_lista.html', {
        'feedbacks': feedbacks
    })


def detalhe_feedback(request, id):
    feedback = Feedback.objects.get(id=id)

    return render(request, 'suporte/feedback_detalhe.html', {
        'feedback': feedback
    })

def criar_feedback(request):
    form = FeedbackForm(request.POST or None)

    if form.is_valid():
        form.save()
        feedbacks = Feedback.objects.all()

        return render(request, 'suporte/feedback_lista.html', {
            'feedbacks': feedbacks
        })

    return render(request, 'suporte/feedback_form.html', {
        'form': form
    })


def editar_feedback(request, id):
    feedback = Feedback.objects.get(id=id)

    form = FeedbackForm(
        request.POST or None,
        instance=feedback
    )

    if form.is_valid():
        form.save()
        feedbacks = Feedback.objects.all()

        return render(request, 'suporte/feedback_lista.html', {
            'feedbacks': feedbacks
        })

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
        avaliacoes = Avaliacao.objects.all()

        return render(request, 'suporte/avaliacao_lista.html', {
            'avaliacoes': avaliacoes
        })

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
        form.save()
        avaliacoes = Avaliacao.objects.all()

        return render(request, 'suporte/avaliacao_lista.html', {
            'avaliacoes': avaliacoes
        })

    return render(request, 'suporte/avaliacao_form.html', {
        'form': form
    })


def deletar_avaliacao(request, id):
    avaliacao = Avaliacao.objects.get(id=id)

    if request.method == 'POST':
        avaliacao.delete()

        return redirect('lista_avaliacoes')

    return render(request, 'suporte/confirmar_delete.html', {
        'objeto': avaliacao,
        'lista_url': 'lista_avaliacoes'
    })