from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.db.models import Avg, Count, ProtectedError, Q
from django.utils.http import (
    url_has_allowed_host_and_scheme,

    urlsafe_base64_decode,
)
from .models import Perfil, Profissional
from .forms import (
    ClienteCadastroForm,
    PerfilForm,
    ProfissionalCadastroForm,
    ProfissionalForm,

)
from .permissoes import (
    GRUPO_CLIENTE,
    GRUPO_PROFISSIONAL,
    adicionar_ao_grupo,
    eh_administrador,
    eh_profissional,
    pode_gerenciar,
)
from interacoes.models import Solicitacao, StatusSolicitacao
from servicos.models import Categoria, Servico
from suporte.models import Feedback, StatusFeedback, TipoAutorAvaliacao


def home(request):
    # Página inicial com destaques (RF018) no formato de dashboard.
    contexto = {
        'total_servicos': Servico.objects.filter(ativo=True).count(),
        'total_profissionais': Profissional.objects.count(),
        'total_categorias': Categoria.objects.count(),

        'servicos': Servico.objects.filter(
            ativo=True
        ).order_by('-data_cadastro')[:6],

        'categorias': Categoria.objects.annotate(
            qtd_servicos=Count('servicos', filter=Q(servicos__ativo=True))
        ).order_by('-qtd_servicos', 'nome')[:6],

        'profissionais': Profissional.objects.order_by('-date_joined')[:5],
    }

    if request.user.is_authenticated:
        if eh_administrador(request.user):
            solicitacoes = Solicitacao.objects.all()
            contexto['rotulo_solicitacoes'] = 'Solicitações pendentes'
        elif eh_profissional(request.user):
            solicitacoes = Solicitacao.objects.filter(
                servico__profissional_id=request.user.id
            )
            contexto['rotulo_solicitacoes'] = 'Pedidos esperando resposta'
        else:
            solicitacoes = Solicitacao.objects.filter(cliente=request.user)
            contexto['rotulo_solicitacoes'] = 'Minhas solicitações pendentes'

        contexto['solicitacoes_pendentes'] = solicitacoes.filter(
            status=StatusSolicitacao.PENDENTE
        ).count()

        contexto['ultimas_solicitacoes'] = solicitacoes.order_by(
            '-data_solicitacao'
        )[:5]

        if request.user.has_perm('suporte.view_feedback'):
            contexto['feedbacks_pendentes'] = Feedback.objects.filter(
                status=StatusFeedback.PENDENTE
            ).count()

    return render(request, 'usuarios/home.html', contexto)


def lista_profissionais(request):
    profissionais = Profissional.objects.all()

    return render(request, 'usuarios/lista.html', {
        'profissionais': profissionais
    })


def detalhe_profissional(request, id):
    profissional = Profissional.objects.get(id=id)

    # Só as avaliações que os clientes fizeram sobre o profissional.
    avaliacoes = profissional.avaliacoes_profissional.filter(
        tipo_autor=TipoAutorAvaliacao.CLIENTE
    ).order_by('-data_avaliacao')

    return render(request, 'usuarios/detalhe.html', {
        'profissional': profissional,
        'perfil': Perfil.do_usuario(profissional),
        'avaliacoes': avaliacoes,
        'media_notas': avaliacoes.aggregate(media=Avg('nota'))['media']
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

        messages.success(request, 'Cadastro concluído! Agora publique o seu primeiro serviço.')

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

        messages.success(request, 'Perfil atualizado.')

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

        messages.success(request, 'Profissional excluído.')

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
        usuario = form.get_user()
        login(request, usuario)

        messages.success(
            request,
            f'Bem-vindo, {usuario.first_name or usuario.username}!'
        )

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


@login_required
def sair(request):
    if request.method == 'POST':
        logout(request)

        messages.info(request, 'Você saiu da sua conta.')

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

        messages.success(request, 'Cadastro concluído! Já pode solicitar serviços.')

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

        messages.success(request, 'Senha alterada.')

        return redirect('minha_conta')

    return render(request, 'usuarios/senha_form.html', {
        'form': form,
        'titulo': 'Alterar senha'
    })


def redefinir_senha(request):
    form = PasswordResetForm(request.POST or None)

    if form.is_valid():
        # Gera o token do django.contrib.auth e envia o link
        # por e-mail (no projeto, o e-mail aparece no terminal).
        form.save(
            request=request,
            use_https=request.is_secure(),
            subject_template_name='usuarios/email_redefinir_senha_assunto.txt',
            email_template_name='usuarios/email_redefinir_senha.txt'
        )

        return redirect('redefinir_senha_enviado')

    return render(request, 'usuarios/senha_form.html', {
        'form': form,
        'titulo': 'Redefinir senha'
    })


def redefinir_senha_enviado(request):
    return render(request, 'usuarios/redefinir_senha_enviado.html')


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


@login_required
def excluir_conta(request):
    if request.method == 'POST':
        usuario = request.user

        try:
            usuario.delete()
        except ProtectedError:
            return render(request, 'usuarios/excluir_conta.html', {
                'erro': 'Não é possível excluir sua conta porque existem solicitações vinculadas aos seus serviços.'
            })

        logout(request)

        messages.success(request, 'Sua conta foi excluída.')

        return redirect('home')

    return render(request, 'usuarios/excluir_conta.html')


@login_required
def minha_conta(request):
    return render(request, 'usuarios/minha_conta.html', {
        'grupos': request.user.groups.all()
    })

@login_required
def personalizar_perfil(request):
    perfil = Perfil.do_usuario(request.user)

    form = PerfilForm(
        request.POST or None,
        request.FILES or None,
        instance=perfil
    )

    if form.is_valid():
        form.save()

        messages.success(request, 'Perfil atualizado! Veja como ficou.')

        return redirect('minha_conta')

    return render(request, 'usuarios/perfil_form.html', {
        'form': form,
        'perfil': perfil
    })