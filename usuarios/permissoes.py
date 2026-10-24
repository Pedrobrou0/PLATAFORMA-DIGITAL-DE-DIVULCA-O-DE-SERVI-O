from django.contrib.auth.models import Group


# Grupos (django.contrib.auth.models.Group) que representam os atores
# do Documento de Casos de Uso. O Visitante é o usuário não autenticado,
# por isso não tem grupo.

GRUPO_CLIENTE = 'Cliente'
GRUPO_PROFISSIONAL = 'Profissional'
GRUPO_ADMINISTRADOR = 'Administrador'


# Permissões (django.contrib.auth.models.Permission) de cada grupo.
# O formato é 'app_label.codename', o mesmo usado em
# @permission_required e em user.has_perm().

PERMISSOES_POR_GRUPO = {
    GRUPO_CLIENTE: [
        # Solicitar Serviço / Acompanhar Solicitações
        'interacoes.add_solicitacao',
        'interacoes.view_solicitacao',

        # Avaliar Usuário
        'suporte.add_avaliacao',
        'suporte.change_avaliacao',
        'suporte.delete_avaliacao',

        # Enviar Feedback
        'suporte.add_feedback',
    ],

    GRUPO_PROFISSIONAL: [
        # Manter Serviços
        'servicos.add_servico',
        'servicos.change_servico',
        'servicos.delete_servico',
        'servicos.view_servico',

        # Gerenciar Solicitações Recebidas
        'interacoes.change_solicitacao',
        'interacoes.view_solicitacao',

        # Avaliar Usuário
        'suporte.add_avaliacao',
        'suporte.change_avaliacao',
        'suporte.delete_avaliacao',

        # Enviar Feedback
        'suporte.add_feedback',
    ],

    GRUPO_ADMINISTRADOR: [
        # Manter Categoria
        'servicos.add_categoria',
        'servicos.change_categoria',
        'servicos.delete_categoria',
        'servicos.view_categoria',

        # Moderação de serviços
        'servicos.change_servico',
        'servicos.delete_servico',

        # Gerenciar Feedbacks
        'suporte.view_feedback',
        'suporte.change_feedback',
        'suporte.delete_feedback',

        # Moderação de solicitações
        'interacoes.view_solicitacao',
        'interacoes.delete_solicitacao',

        # Gerenciar Usuários
        'usuarios.change_profissional',
        'usuarios.delete_profissional',
        'auth.view_user',
        'auth.change_user',
        'auth.delete_user',
    ],
}


def adicionar_ao_grupo(usuario, nome_grupo):
    grupo, _ = Group.objects.get_or_create(name=nome_grupo)
    usuario.groups.add(grupo)


def eh_profissional(usuario):
    return usuario.is_authenticated and hasattr(usuario, 'profissional')


def eh_cliente(usuario):
    return usuario.is_authenticated and usuario.groups.filter(
        name=GRUPO_CLIENTE
    ).exists()


def eh_administrador(usuario):
    if not usuario.is_authenticated:
        return False

    return usuario.is_superuser or usuario.groups.filter(
        name=GRUPO_ADMINISTRADOR
    ).exists()


def pode_gerenciar(usuario, dono_id):
    # Dono do objeto ou Administrador (moderação).
    return usuario.id == dono_id or eh_administrador(usuario)
