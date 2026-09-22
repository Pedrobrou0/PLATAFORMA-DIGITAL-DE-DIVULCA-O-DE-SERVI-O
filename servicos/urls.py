from django.urls import path
from . import views


urlpatterns = [
    path(
        'categorias/',
        views.lista_categorias,
        name='lista_categorias'
    ),

    path(
        'categorias/novo/',
        views.criar_categoria,
        name='criar_categoria'
    ),

    path(
        'categorias/<int:id>/',
        views.detalhe_categoria,
        name='detalhe_categoria'
    ),

    path(
        'categorias/<int:id>/editar/',
        views.editar_categoria,
        name='editar_categoria'
    ),

    path(
        'categorias/<int:id>/deletar/',
        views.deletar_categoria,
        name='deletar_categoria'
    ),

    path(
        'servicos/',
        views.lista_servicos,
        name='lista_servicos'
    ),

    path(
        'servicos/novo/',
        views.criar_servico,
        name='criar_servico'
    ),

    path(
        'servicos/<int:id>/',
        views.detalhe_servico,
        name='detalhe_servico'
    ),

    path(
        'servicos/<int:id>/editar/',
        views.editar_servico,
        name='editar_servico'
    ),

    path(
        'servicos/<int:id>/deletar/',
        views.deletar_servico,
        name='deletar_servico'
    ),

    path(
        'servicos/<int:id>/ativar/',
        views.ativar_servico,
        name='ativar_servico'
    ),

    path(
        'servicos/<int:id>/desativar/',
        views.desativar_servico,
        name='desativar_servico'
    ),
]