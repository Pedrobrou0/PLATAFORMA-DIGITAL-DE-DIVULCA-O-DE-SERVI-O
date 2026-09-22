from django.shortcuts import render, redirect
from .models import Categoria, Servico
from .forms import CategoriaForm, ServicoForm


def lista_categorias(request):
    categorias = Categoria.objects.all()

    return render(request, 'servicos/categoria_lista.html', {
        'categorias': categorias
    })


def deletar_categoria(request, id):
    categoria = Categoria.objects.get(id=id)

    if request.method == 'POST':
        categoria.delete()

        return redirect('lista_categorias')

    return render(request, 'servicos/confirmar_delete.html', {
        'objeto': categoria,
        'lista_url': 'lista_categorias'
    })


def criar_categoria(request):
    form = CategoriaForm(request.POST or None)

    if form.is_valid():
        form.save()
        categorias = Categoria.objects.all()

        return render(request, 'servicos/categoria_lista.html', {
            'categorias': categorias
        })

    return render(request, 'servicos/categoria_form.html', {
        'form': form
    })


def editar_categoria(request, id):
    categoria = Categoria.objects.get(id=id)

    form = CategoriaForm(
        request.POST or None,
        instance=categoria
    )

    if form.is_valid():
        form.save()
        categorias = Categoria.objects.all()

        return render(request, 'servicos/categoria_lista.html', {
            'categorias': categorias
        })

    return render(request, 'servicos/categoria_form.html', {
        'form': form
    })


def detalhe_categoria(request, id):
    categoria = Categoria.objects.get(id=id)

    profissionais = categoria.profissionais.all()

    servicos = Servico.objects.filter(
        categoria=categoria
    )

    return render(request, 'servicos/categoria_detalhe.html', {
        'categoria': categoria,
        'profissionais': profissionais,
        'servicos': servicos
    })

def lista_servicos(request):
    categoria_id = request.GET.get('categoria')
    termo = request.GET.get('q')

    servicos = Servico.objects.all()

    if categoria_id:
        servicos = servicos.filter(categoria_id=categoria_id)

    if termo:
        servicos = servicos.filter(titulo__icontains=termo)

    categorias = Categoria.objects.all()

    return render(request, 'servicos/servico_lista.html', {
        'servicos': servicos,
        'categorias': categorias,
        'categoria_selecionada': categoria_id,
        'termo': termo
    })


def detalhe_servico(request, id):
    servico = Servico.objects.get(id=id)

    return render(request, 'servicos/servico_detalhe.html', {
        'servico': servico
    })


def criar_servico(request):
    form = ServicoForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():
        form.save()
        servicos = Servico.objects.all()

        return render(request, 'servicos/servico_lista.html', {
            'servicos': servicos
        })

    return render(request, 'servicos/servico_form.html', {
        'form': form
    })


def editar_servico(request, id):
    servico = Servico.objects.get(id=id)

    form = ServicoForm(
        request.POST or None,
        request.FILES or None,
        instance=servico
    )

    if form.is_valid():
        form.save()
        servicos = Servico.objects.all()

        return render(request, 'servicos/servico_lista.html', {
            'servicos': servicos
        })

    return render(request, 'servicos/servico_form.html', {
        'form': form
    })


def deletar_servico(request, id):
    servico = Servico.objects.get(id=id)

    if request.method == 'POST':
        servico.delete()

        return redirect('lista_servicos')

    return render(request, 'servicos/confirmar_delete.html', {
        'objeto': servico,
        'lista_url': 'lista_servicos'
    })

def ativar_servico(request, id):
    servico = Servico.objects.get(id=id)

    if request.method == 'POST':
        servico.ativar()

    return redirect('detalhe_servico', id=servico.id)


def desativar_servico(request, id):
    servico = Servico.objects.get(id=id)

    if request.method == 'POST':
        servico.desativar()

    return redirect('detalhe_servico', id=servico.id)