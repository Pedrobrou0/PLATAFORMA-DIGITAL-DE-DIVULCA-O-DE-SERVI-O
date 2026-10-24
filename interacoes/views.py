from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from .models import Solicitacao, StatusSolicitacao
from .forms import SolicitacaoForm, SolicitacaoEditarForm


def lista_solicitacoes(request):
    solicitacoes = Solicitacao.objects.all()

    return render(request, 'interacoes/lista.html', {
        'solicitacoes': solicitacoes
    })


def detalhe_solicitacao(request, id):
    solicitacao = Solicitacao.objects.get(id=id)

    return render(request, 'interacoes/detalhe.html', {
        'solicitacao': solicitacao
    })


@login_required
@permission_required('interacoes.add_solicitacao', raise_exception=True)
def criar_solicitacao(request):
    servico_id = request.GET.get('servico')

    form = SolicitacaoForm(
        request.POST or None,
        initial={
            'servico': servico_id
        }
    )

    if form.is_valid():
        solicitacao = form.save(commit=False)

        # O cliente é sempre quem está logado.
        solicitacao.cliente = request.user
        solicitacao.save()

        return redirect('detalhe_solicitacao', id=solicitacao.id)

    return render(request, 'interacoes/form.html', {
        'form': form
    })


def editar_solicitacao(request, id):
    solicitacao = Solicitacao.objects.get(id=id)

    form = SolicitacaoEditarForm(
        request.POST or None,
        instance=solicitacao
    )

    if form.is_valid():
        form.save()

        return redirect('lista_solicitacoes')

    return render(request, 'interacoes/form.html', {
        'form': form
    })


def deletar_solicitacao(request, id):
    solicitacao = Solicitacao.objects.get(id=id)

    if request.method == 'POST':
        solicitacao.delete()

        return redirect('lista_solicitacoes')

    return render(request, 'interacoes/confirmar_delete.html', {
        'objeto': solicitacao,
        'lista_url': 'lista_solicitacoes'
    })

def aceitar_solicitacao(request, id):
    solicitacao = Solicitacao.objects.get(id=id)

    if request.method == 'POST' and solicitacao.status == StatusSolicitacao.PENDENTE:
        solicitacao.aceitar()

    return redirect('detalhe_solicitacao', id=solicitacao.id)


def recusar_solicitacao(request, id):
    solicitacao = Solicitacao.objects.get(id=id)

    if request.method == 'POST' and solicitacao.status == StatusSolicitacao.PENDENTE:
        solicitacao.recusar()

    return redirect('detalhe_solicitacao', id=solicitacao.id)


def cancelar_solicitacao(request, id):
    solicitacao = Solicitacao.objects.get(id=id)

    if request.method == 'POST' and solicitacao.status in [
        StatusSolicitacao.PENDENTE,
        StatusSolicitacao.ACEITA
    ]:
        solicitacao.cancelar()

    return redirect('detalhe_solicitacao', id=solicitacao.id)


def concluir_solicitacao(request, id):
    solicitacao = Solicitacao.objects.get(id=id)

    if request.method == 'POST' and solicitacao.status == StatusSolicitacao.ACEITA:
        solicitacao.concluir()

    return redirect('detalhe_solicitacao', id=solicitacao.id)