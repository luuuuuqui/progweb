from django.shortcuts import render, get_object_or_404, redirect
from core.models.categoria import Categoria

def list_categoria_view(request):
    categorias = Categoria.objects.all()
    context = {
        'categorias': categorias
    }
    return render(request, template_name='categoria/categoria.html', context=context, status=200)

def create_categoria_view(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        if nome:
            categoria = Categoria(nome=nome)
            categoria.save()
        return redirect('categoria')
        
    return render(request, template_name='categoria/categoria-edit.html')

def edit_categoria_view(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == "POST":
        nome = request.POST.get("nome")
        if nome:
            categoria.nome = nome
            categoria.save()
        return redirect('categoria')
        
    context = {
        'categoria': categoria
    }
    return render(request, template_name='categoria/categoria-edit.html', context=context)

def delete_categoria_view(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    return redirect('categoria')
