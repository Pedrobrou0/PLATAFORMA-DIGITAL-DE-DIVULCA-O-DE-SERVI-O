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