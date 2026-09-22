from django.shortcuts import render, redirect
from .models import Profissional
from .forms import ProfissionalForm
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
        profissionais = Profissional.objects.all()

        return render(request, 'usuarios/lista.html', {
            'profissionais': profissionais
        })

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
        profissionais = Profissional.objects.all()

        return render(request, 'usuarios/lista.html', {
            'profissionais': profissionais
        })

    return render(request, 'usuarios/form.html', {
        'form': form
    })


def deletar_profissional(request, id):
    profissional = Profissional.objects.get(id=id)

    if request.method == 'POST':
        profissional.delete()

        return redirect('lista_profissionais')

    return render(request, 'usuarios/confirmar_delete.html', {
        'objeto': profissional,
        'lista_url': 'lista_profissionais'
    })