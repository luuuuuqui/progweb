from datetime import timedelta
from decimal import Decimal
from typing import Any, cast

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from core.models.categoria import Categoria
from core.models.fabricante import Fabricante
from core.models.produto import Produto


def list_produto_view(request: HttpRequest, id: int | None = None) -> HttpResponse:
    produto = request.GET.get("produto")
    destaque = request.GET.get("destaque")
    promocao = request.GET.get("promocao")
    categoria = request.GET.get("categoria")
    fabricante = request.GET.get("fabricante")
    dias = request.GET.get("dias")

    produtos = cast(Any, Produto.objects.all())

    if id is not None:
        produtos = produtos.filter(id=id)

    if produto is not None:
        produtos = produtos.filter(nome__contains=produto)

    if destaque is not None:
        produtos = produtos.filter(destaque=destaque)

    if promocao is not None:
        produtos = produtos.filter(promocao=promocao)

    if categoria is not None:
        produtos = produtos.filter(categoria__nome=categoria)

    if fabricante is not None:
        produtos = produtos.filter(fabricante__nome=fabricante)

    if dias is not None:
        now = timezone.now() - timedelta(days=int(dias))
        produtos = produtos.filter(criado_em__gte=now)

    context = {"produtos": produtos}
    return render(
        request, template_name="produto/produto.html", context=context, status=200
    )


def edit_produto_view(request: HttpRequest, id: int) -> HttpResponse:
    produto = get_object_or_404(Produto, id=id)

    if request.method == "POST":
        nome = request.POST.get("Produto", "")
        destaque = request.POST.get("destaque") == "on"
        promocao = request.POST.get("promocao") == "on"
        msg_promocao = request.POST.get("msgPromocao")
        categoria_id = request.POST.get("CategoriaFk")
        fabricante_id = request.POST.get("FabricanteFk")
        preco = request.POST.get("preco")
        foto = request.FILES.get("foto")

        produto.nome = nome
        produto.destaque = destaque
        produto.promocao = promocao
        produto.msg_promocao = msg_promocao

        if foto is not None:
            produto.foto = foto

        if preco:
            produto.preco = Decimal(preco)

        if categoria_id and categoria_id != "-1":
            produto.categoria = get_object_or_404(Categoria, id=int(categoria_id))
        else:
            produto.categoria = None

        if fabricante_id and fabricante_id != "-1":
            produto.fabricante = get_object_or_404(
                Fabricante,
                id=int(fabricante_id),
            )
        else:
            produto.fabricante = None

        produto.save()
        return redirect("produto")

    categorias = cast(Any, Categoria.objects.all())
    fabricantes = cast(Any, Fabricante.objects.all())

    context = {
        "produto": produto,
        "categorias": categorias,
        "fabricantes": fabricantes,
    }
    return render(request, template_name="produto/produto-edit.html", context=context)


def delete_produto_view(request: HttpRequest, id: int) -> HttpResponse:
    produto = get_object_or_404(Produto, id=id)

    if request.method == "POST":
        if produto.foto:
            produto.foto.delete(save=False)

        produto.delete()
        return redirect("produto")

    context = {"produto": produto}
    return render(request, template_name="produto/produto-delete.html", context=context)


def create_produto_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        nome = request.POST.get("Produto", "")
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
            preco=Decimal(preco),
        )

        if foto is not None:
            produto.foto = foto

        if categoria_id and categoria_id != "-1":
            produto.categoria = get_object_or_404(Categoria, id=int(categoria_id))

        if fabricante_id and fabricante_id != "-1":
            produto.fabricante = get_object_or_404(
                Fabricante,
                id=int(fabricante_id),
            )

        produto.save()
        return redirect("produto")

    categorias = cast(Any, Categoria.objects.all())
    fabricantes = cast(Any, Fabricante.objects.all())

    context = {
        "categorias": categorias,
        "fabricantes": fabricantes,
    }
    return render(request, template_name="produto/produto-edit.html", context=context)


def details_produto_view(request: HttpRequest, id: int) -> HttpResponse:
    produto = get_object_or_404(Produto, id=id)
    context = {"produto": produto}
    return render(
        request, template_name="produto/produto-details.html", context=context
    )
