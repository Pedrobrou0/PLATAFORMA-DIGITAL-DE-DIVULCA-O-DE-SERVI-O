from django.urls import path
from . import views


urlpatterns = [
    path(
        'feedbacks/',
        views.lista_feedbacks,
        name='lista_feedbacks'
    ),

    path(
        'feedbacks/novo/',
        views.criar_feedback,
        name='criar_feedback'
    ),

    path(
        'feedbacks/<int:id>/',
        views.detalhe_feedback,
        name='detalhe_feedback'
    ),

    path(
        'feedbacks/<int:id>/editar/',
        views.editar_feedback,
        name='editar_feedback'
    ),

    path(
        'feedbacks/<int:id>/deletar/',
        views.deletar_feedback,
        name='deletar_feedback'
    ),


path(
        'avaliacoes/',
        views.lista_avaliacoes,
        name='lista_avaliacoes'
    ),

    path(
        'avaliacoes/novo/',
        views.criar_avaliacao,
        name='criar_avaliacao'
    ),

    path(
        'avaliacoes/<int:id>/',
        views.detalhe_avaliacao,
        name='detalhe_avaliacao'
    ),

    path(
        'avaliacoes/<int:id>/editar/',
        views.editar_avaliacao,
        name='editar_avaliacao'
    ),

    path(
        'avaliacoes/<int:id>/deletar/',
        views.deletar_avaliacao,
        name='deletar_avaliacao'
    ),

]