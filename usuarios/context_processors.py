from .models import Perfil


def perfil(request):
    """Deixa {{ meu_perfil }} disponível em todos os templates.

    É assim que a foto e a cor escolhidas pelo usuário aparecem
    no topo e no menu lateral, em qualquer página do site.
    """
    if request.user.is_authenticated:
        return {'meu_perfil': Perfil.do_usuario(request.user)}

    return {}
