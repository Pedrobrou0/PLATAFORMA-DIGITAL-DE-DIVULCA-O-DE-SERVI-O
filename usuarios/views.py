from django.conf import settings
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    SetPasswordForm,
)
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.db.models import ProtectedError
from django.utils.http import (
    url_has_allowed_host_and_scheme,
    urlsafe_base64_decode,
)
from .models import Profissional
from .forms import (

    ClienteCadastroForm,
    ProfissionalCadastroForm,
    ProfissionalForm,
)
from .permissoes import (
    GRUPO_CLIENTE,
    GRUPO_PROFISSIONAL,
    adicionar_ao_grupo,
    pode_gerenciar,
)
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
    if request.user.is_authenticated:
        return redirect('home')

    form = ProfissionalCadastroForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():
        profissional = form.save()

        adicionar_ao_grupo(profissional, GRUPO_PROFISSIONAL)

        login(request, profissional)

        return redirect('detalhe_profissional', id=profissional.id)

    return render(request, 'usuarios/cadastro_form.html', {
        'form': form,
        'titulo': 'Cadastro de profissional'
    })


@login_required
def editar_profissional(request, id):
    profissional = Profissional.objects.get(id=id)

    if not pode_gerenciar(request.user, profissional.id):
        raise PermissionDenied

    form = ProfissionalForm(
        request.POST or None,
        request.FILES or None,
        instance=profissional
    )

    if form.is_valid():
       form.save()

    return redirect('detalhe_profissional', id=profissional.id)

    return render(request, 'usuarios/form.html', {
        'form': form
    })


@login_required
def deletar_profissional(request, id):
    profissional = Profissional.objects.get(id=id)

    if not pode_gerenciar(request.user, profissional.id):
        raise PermissionDenied

    if request.method == 'POST':
        proprio_usuario = request.user.id == profissional.id

        try:
            profissional.delete()
        except ProtectedError:
            return render(request, 'usuarios/confirmar_delete.html', {
                'objeto': profissional,
                'lista_url': 'lista_profissionais',
                'erro': 'Não é possível excluir este profissional porque existem solicitações vinculadas aos serviços dele.'
            })

        if proprio_usuario:
            logout(request)

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

@login_required
def alterar_senha(request):
    form = PasswordChangeForm(
        request.user,
        request.POST or None
    )

    if form.is_valid():
        usuario = form.save()

        # Mantém o usuário logado depois de trocar a senha.
        update_session_auth_hash(request, usuario)

        return redirect('home')

    return render(request, 'usuarios/senha_form.html', {
        'form': form,
        'titulo': 'Alterar senha'
    })


def confirmar_redefinicao_senha(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        usuario = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        usuario = None

    # O token do django.contrib.auth expira e só vale uma vez.
    link_valido = (
        usuario is not None
        and default_token_generator.check_token(usuario, token)
    )

    form = None

    if link_valido:
        form = SetPasswordForm(usuario, request.POST or None)

        if form.is_valid():
            form.save()

            return redirect('redefinir_senha_concluido')

    return render(request, 'usuarios/confirmar_redefinicao_senha.html', {
        'form': form,
        'link_valido': link_valido
    })


def redefinir_senha_concluido(request):
    return render(request, 'usuarios/redefinir_senha_concluido.html')
