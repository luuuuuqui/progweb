from datetime import timedelta

from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from core.models.categoria import Categoria
from core.models.fabricante import Fabricante
from core.models.produto import Produto


def list_produto_view(request):
    # Capturando os parâmetros da URL
    produto = request.GET.get("produto")
    categoria = request.GET.get("categoria")
    dias = request.GET.get("dias")

    # 2. Comando para pegar todos os produtos do banco
    produtos = Produto.objects.all()

    # 3. Aplicando os filtros ensinados no PDF
    if produto is not None:
        # Filtro por aproximação de texto (like)
        produtos = produtos.filter(nome__contains=produto)

    if categoria is not None:
        # Filtro por chave estrangeira
        produtos = produtos.filter(categoria__nome=categoria)

    if dias is not None:
        # Filtro de datas (maior ou igual a X dias atrás)
        now = timezone.now()
        now = now - timedelta(days=int(dias))
        produtos = produtos.filter(criado_em__gte=now)

    # Imprime no terminal onde o servidor está rodando
    print(produtos)

    context = {"produtos": produtos}
    return render(
        request, template_name="produto/produto.html", context=context, status=200
    )


def edit_produto_view(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == "POST":
        # Get data from post
        nome = request.POST.get("Produto")
        destaque = request.POST.get("destaque") == "on"
        promocao = request.POST.get("promocao") == "on"
        msg_promocao = request.POST.get("msgPromocao")
        categoria_id = request.POST.get("CategoriaFk")
        fabricante_id = request.POST.get("FabricanteFk")
        preco = request.POST.get("preco")
        foto = request.FILES.get("foto")

        # Update product fields
        produto.nome = nome
        produto.destaque = destaque
        produto.promocao = promocao
        produto.msg_promocao = msg_promocao

        if foto:
            produto.foto = foto

        if preco:
            produto.preco = preco

        if categoria_id and categoria_id != "-1":
            produto.categoria_id = int(categoria_id)
        else:
            produto.categoria = None

        if fabricante_id and fabricante_id != "-1":
            produto.fabricante_id = int(fabricante_id)
        else:
            produto.fabricante = None

        produto.save()
        return redirect("produto")

    categorias = Categoria.objects.all()
    fabricantes = Fabricante.objects.all()

    context = {
        "produto": produto,
        "categorias": categorias,
        "fabricantes": fabricantes,
    }
    return render(request, template_name="produto/produto-edit.html", context=context)


def delete_produto_view(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    return redirect("produto")


def create_produto_view(request):
    if request.method == "POST":
        nome = request.POST.get("Produto")
        destaque = request.POST.get("destaque") == "on"
        promocao = request.POST.get("promocao") == "on"
        msg_promocao = request.POST.get("msgPromocao")
        categoria_id = request.POST.get("CategoriaFk")
        fabricante_id = request.POST.get("FabricanteFk")
        preco = request.POST.get("preco") or "0.00"
        foto = request.FILES.get("foto")

        produto = Produto(
            nome=nome,
            destaque=destaque,
            promocao=promocao,
            msg_promocao=msg_promocao,
            preco=preco,
        )

        if foto:
            produto.foto = foto

        if categoria_id and categoria_id != "-1":
            produto.categoria_id = int(categoria_id)
        if fabricante_id and fabricante_id != "-1":
            produto.fabricante_id = int(fabricante_id)

        produto.save()
        return redirect("produto")

    categorias = Categoria.objects.all()
    fabricantes = Fabricante.objects.all()

    context = {
        "categorias": categorias,
        "fabricantes": fabricantes,
    }
    return render(request, template_name="produto/produto-edit.html", context=context)


def details_produto_view(request, id):
    produto = get_object_or_404(Produto, id=id)
    context = {"produto": produto}
    return render(
        request, template_name="produto/produto-details.html", context=context
    )
