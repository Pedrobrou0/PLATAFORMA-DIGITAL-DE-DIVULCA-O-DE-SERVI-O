from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from .models import Solicitacao, StatusSolicitacao
from .forms import SolicitacaoForm, SolicitacaoEditarForm
from usuarios.permissoes import eh_administrador, eh_profissional


def verificar_cliente_dono(request, solicitacao):
    if solicitacao.cliente_id != request.user.id:
        raise PermissionDenied


def verificar_profissional_dono(request, solicitacao):
    if solicitacao.servico.profissional_id != request.user.id:
        raise PermissionDenied


@login_required
def lista_solicitacoes(request):
    if eh_administrador(request.user):
        solicitacoes = Solicitacao.objects.all()
        titulo = 'Todas as solicitações'

    elif eh_profissional(request.user):
        # Gerenciar Solicitações Recebidas
        solicitacoes = Solicitacao.objects.filter(
            servico__profissional_id=request.user.id
        )
        titulo = 'Solicitações recebidas'

    else:
        # Acompanhar Solicitações
        solicitacoes = Solicitacao.objects.filter(
            cliente=request.user
        )
        titulo = 'Minhas solicitações'

    return render(request, 'interacoes/lista.html', {
        'solicitacoes': solicitacoes.order_by('-data_solicitacao'),
        'titulo': titulo
    })


@login_required
def detalhe_solicitacao(request, id):
    solicitacao = Solicitacao.objects.get(id=id)

    eh_cliente_dono = solicitacao.cliente_id == request.user.id
    eh_profissional_dono = (
        solicitacao.servico.profissional_id == request.user.id
    )

    if not (
        eh_cliente_dono
        or eh_profissional_dono
        or eh_administrador(request.user)
    ):
        raise PermissionDenied

    return render(request, 'interacoes/detalhe.html', {
        'solicitacao': solicitacao,
        'eh_cliente_dono': eh_cliente_dono,
        'eh_profissional_dono': eh_profissional_dono
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


@login_required
def editar_solicitacao(request, id):
    solicitacao = Solicitacao.objects.get(id=id)

    verificar_cliente_dono(request, solicitacao)

    # Só dá para editar enquanto o profissional não respondeu.
    if solicitacao.status != StatusSolicitacao.PENDENTE:
        return redirect('detalhe_solicitacao', id=solicitacao.id)

    form = SolicitacaoEditarForm(
        request.POST or None,
        instance=solicitacao
    )

    if form.is_valid():
        form.save()

        return redirect('detalhe_solicitacao', id=solicitacao.id)

    return render(request, 'interacoes/form.html', {
        'form': form
    })


@login_required
@permission_required('interacoes.delete_solicitacao', raise_exception=True)
def deletar_solicitacao(request, id):
    solicitacao = Solicitacao.objects.get(id=id)

    if request.method == 'POST':
        solicitacao.delete()

        return redirect('lista_solicitacoes')

    return render(request, 'interacoes/confirmar_delete.html', {
        'objeto': solicitacao,
        'lista_url': 'lista_solicitacoes'
    })

@login_required
@permission_required('interacoes.change_solicitacao', raise_exception=True)
def aceitar_solicitacao(request, id):
    solicitacao = Solicitacao.objects.get(id=id)

    verificar_profissional_dono(request, solicitacao)

    if request.method == 'POST' and solicitacao.status == StatusSolicitacao.PENDENTE:
        solicitacao.aceitar()

    return redirect('detalhe_solicitacao', id=solicitacao.id)


@login_required
@permission_required('interacoes.change_solicitacao', raise_exception=True)
def recusar_solicitacao(request, id):
    solicitacao = Solicitacao.objects.get(id=id)

    verificar_profissional_dono(request, solicitacao)

    if request.method == 'POST' and solicitacao.status == StatusSolicitacao.PENDENTE:
        solicitacao.recusar()

    return redirect('detalhe_solicitacao', id=solicitacao.id)


@login_required
def cancelar_solicitacao(request, id):
    solicitacao = Solicitacao.objects.get(id=id)

    verificar_cliente_dono(request, solicitacao)

    if request.method == 'POST' and solicitacao.status in [
        StatusSolicitacao.PENDENTE,
        StatusSolicitacao.ACEITA
    ]:
        solicitacao.cancelar()

    return redirect('detalhe_solicitacao', id=solicitacao.id)


@login_required
@permission_required('interacoes.change_solicitacao', raise_exception=True)
def concluir_solicitacao(request, id):
    solicitacao = Solicitacao.objects.get(id=id)

    verificar_profissional_dono(request, solicitacao)

    if request.method == 'POST' and solicitacao.status == StatusSolicitacao.ACEITA:
        solicitacao.concluir()

    return redirect('detalhe_solicitacao', id=solicitacao.id)