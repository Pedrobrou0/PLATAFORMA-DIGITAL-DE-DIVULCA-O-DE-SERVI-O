from django.urls import path
from . import views


urlpatterns = [
    path(
        '',
        views.home,
        name='home'
    ),
    path(
        'profissionais/',
        views.lista_profissionais,
        name='lista_profissionais'
    ),
    path(
        'profissionais/novo/',
        views.criar_profissional,
        name='criar_profissional'
    ),
    path(
        'profissionais/<int:id>/',
        views.detalhe_profissional,
        name='detalhe_profissional'
    ),
    path(
        'profissionais/<int:id>/editar/',
        views.editar_profissional,
        name='editar_profissional'
    ),
    path(
        'profissionais/<int:id>/deletar/',
        views.deletar_profissional,
        name='deletar_profissional'
    ),
]