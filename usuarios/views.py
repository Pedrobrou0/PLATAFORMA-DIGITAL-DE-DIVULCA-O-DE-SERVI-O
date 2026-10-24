from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.db.models import ProtectedError
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Profissional
from .forms import ClienteCadastroForm, ProfissionalForm
from .permissoes import GRUPO_CLIENTE, adicionar_ao_grupo
from servicos.models import Servico


def home(request):
    profissionais = Profissional.objects.all()[:6]
    servicos = Servico.objects.filter(ativo=True)[:6]

    return render(request, 'usuarios/home.html', {
        'profissionais': profissionais,
        'servicos': servicos
    })


def lista_profissionais(request):
    profissionais = Profissional.objects.all()

    return render(request, 'usuarios/lista.html', {
        'profissionais': profissionais
    })


def detalhe_profissional(request, id):
    profissional = Profissional.objects.get(id=id)

    return render(request, 'usuarios/detalhe.html', {
        'profissional': profissional
    })


def criar_profissional(request):
    form = ProfissionalForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():
        form.save()

        return redirect('lista_profissionais')

    return render(request, 'usuarios/form.html', {
        'form': form
    })


def editar_profissional(request, id):
    profissional = Profissional.objects.get(id=id)

    form = ProfissionalForm(
        request.POST or None,
        request.FILES or None,
        instance=profissional
    )

    if form.is_valid():
        form.save()

        return redirect('lista_profissionais')

    return render(request, 'usuarios/form.html', {
        'form': form
    })


def deletar_profissional(request, id):
    profissional = Profissional.objects.get(id=id)

    if request.method == 'POST':
        try:
            profissional.delete()
        except ProtectedError:
            return render(request, 'usuarios/confirmar_delete.html', {
                'objeto': profissional,
                'lista_url': 'lista_profissionais',
                'erro': 'Não é possível excluir este profissional porque existem solicitações vinculadas aos serviços dele.'
            })

        return redirect('lista_profissionais')

    return render(request, 'usuarios/confirmar_delete.html', {
        'objeto': profissional,
        'lista_url': 'lista_profissionais'
    })
def entrar(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = AuthenticationForm(
        request,
        data=request.POST or None
    )

    if form.is_valid():
        login(request, form.get_user())

        proxima = request.POST.get('next') or request.GET.get('next')

        if proxima and url_has_allowed_host_and_scheme(
            proxima,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure()
        ):
            return redirect(proxima)

        return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'usuarios/login.html', {
        'form': form,
        'next': request.GET.get('next', '')
    })

def sair(request):
    if request.method == 'POST':
        logout(request)

    return redirect(settings.LOGOUT_REDIRECT_URL)

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'usuarios/cadastro.html')


def cadastro_cliente(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = ClienteCadastroForm(request.POST or None)

    if form.is_valid():
        cliente = form.save()

        adicionar_ao_grupo(cliente, GRUPO_CLIENTE)

        login(request, cliente)

        return redirect('home')

    return render(request, 'usuarios/cadastro_form.html', {
        'form': form,
        'titulo': 'Cadastro de cliente'
    })
