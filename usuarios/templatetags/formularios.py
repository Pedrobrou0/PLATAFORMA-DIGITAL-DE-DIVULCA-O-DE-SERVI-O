import re

from django import template
from django.forms import (
    CheckboxInput,
    CheckboxSelectMultiple,
    FileInput,
    RadioSelect,
)

register = template.Library()


@register.filter
def bootstrap(campo):
    """Desenha o campo do formulário com a classe certa do Bootstrap 4.

    Uso no template: {% load formularios %} e depois {{ campo|bootstrap }}
    """
    widget = campo.field.widget

    if isinstance(widget, CheckboxInput):
        classe = 'form-check-input'
    elif isinstance(widget, FileInput):
        classe = 'form-control-file'
    elif isinstance(widget, (CheckboxSelectMultiple, RadioSelect)):
        classe = ''
    else:
        classe = 'form-control'

    # Borda vermelha nos campos com erro.
    if campo.errors and classe == 'form-control':
        classe += ' is-invalid'

    classes = f"{widget.attrs.get('class', '')} {classe}".strip()

    return campo.as_widget(attrs={'class': classes})


@register.filter
def whatsapp(telefone):
    """Transforma o telefone em número para o link https://wa.me/ (RF017)."""
    digitos = re.sub(r'\D', '', telefone or '')

    # DDD + número (10 ou 11 dígitos) ganha o código do Brasil.
    if len(digitos) in (10, 11):
        digitos = '55' + digitos

    return digitos