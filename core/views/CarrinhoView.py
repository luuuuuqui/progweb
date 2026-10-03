from typing import Any, cast

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST

from core.models import Carrinho, CarrinhoItem, Produto


def _carrinho_da_sessao(
    request: HttpRequest, *, bloquear: bool = False
) -> Carrinho | None:
    carrinho_id = request.session.get("carrinho_id")
    if not isinstance(carrinho_id, int):
        request.session.pop("carrinho_id", None)
        return None
    carrinhos = Carrinho.objects.filter(
        pk=carrinho_id, situacao=Carrinho.ABERTO, user__isnull=True
    )
    if bloquear:
        carrinhos = carrinhos.select_for_update()
    carrinho = carrinhos.first()
    if carrinho is None:
        request.session.pop("carrinho_id", None)
    return carrinho


@require_POST
@transaction.atomic
def create_carrinhoitem_view(request: HttpRequest, produto_id: int) -> HttpResponse:
    produto = get_object_or_404(Produto, pk=produto_id)
    carrinho = _carrinho_da_sessao(request, bloquear=True)
    if carrinho is None:
        carrinho = Carrinho.objects.create()
        request.session["carrinho_id"] = carrinho.pk
    item, criado = CarrinhoItem.objects.get_or_create(
        carrinho=carrinho,
        produto=produto,
        defaults={"nome_produto": produto.nome, "preco": produto.preco},
    )
    if not criado:
        CarrinhoItem.objects.filter(pk=item.pk).update(quantidade=F("quantidade") + 1)
    return redirect("list_carrinho")


def list_carrinho_view(request: HttpRequest) -> HttpResponse:
    carrinho = _carrinho_da_sessao(request)
    itens: Any = cast(Any, carrinho).itens.select_related("produto") if carrinho else []
    return render(
        request, "carrinho/carrinho-listar.html", {"carrinho": carrinho, "itens": itens}
    )


@require_POST
@transaction.atomic
def alterar_quantidade_view(
    request: HttpRequest, item_id: int, acao: str
) -> HttpResponse:
    carrinho = _carrinho_da_sessao(request, bloquear=True)
    if carrinho is None:
        return redirect("list_carrinho")
    item = get_object_or_404(CarrinhoItem, pk=item_id, carrinho=carrinho)
    if acao == "adicionar":
        if item.produto_id is None:
            messages.warning(request, "Este produto não está mais disponível.")
            return redirect("list_carrinho")
        CarrinhoItem.objects.filter(pk=item.pk).update(quantidade=F("quantidade") + 1)
    elif item.quantidade > 1:
        CarrinhoItem.objects.filter(pk=item.pk).update(quantidade=F("quantidade") - 1)
    else:
        item.delete()
    return redirect("list_carrinho")


@require_POST
@transaction.atomic
def remover_item_view(request: HttpRequest, item_id: int) -> HttpResponse:
    carrinho = _carrinho_da_sessao(request, bloquear=True)
    if carrinho is None:
        return redirect("list_carrinho")
    item = get_object_or_404(CarrinhoItem, pk=item_id, carrinho=carrinho)
    item.delete()
    return redirect("list_carrinho")


@login_required
@require_http_methods(["GET", "POST"])
@transaction.atomic
def confirmar_carrinho_view(request: HttpRequest) -> HttpResponse:
    carrinho = _carrinho_da_sessao(request, bloquear=True)
    if carrinho is None:
        return redirect("list_carrinho")
    itens = cast(Any, carrinho).itens.select_related("produto")
    if not itens.exists():
        messages.warning(request, "Adicione produtos antes de finalizar a compra.")
        return redirect("list_carrinho")
    if itens.filter(produto__isnull=True).exists():
        messages.warning(
            request, "Remova os produtos indisponíveis antes de finalizar."
        )
        return redirect("list_carrinho")
    if request.method == "POST":
        carrinho.user_id = request.user.pk
        carrinho.situacao = Carrinho.CONFIRMADO
        carrinho.confirmado_em = timezone.now()
        carrinho.save(update_fields=["user", "situacao", "confirmado_em"])
        request.session.pop("carrinho_id", None)
        return redirect("carrinho_confirmado", carrinho_id=carrinho.pk)
    return render(
        request,
        "carrinho/carrinho-listar.html",
        {"carrinho": carrinho, "itens": itens, "confirmando": True},
    )


@login_required
def carrinho_confirmado_view(request: HttpRequest, carrinho_id: int) -> HttpResponse:
    carrinho = get_object_or_404(
        Carrinho.objects.prefetch_related("itens"),
        pk=carrinho_id,
        user=request.user,
        situacao=Carrinho.CONFIRMADO,
    )
    return render(
        request,
        "carrinho/carrinho-confirmado.html",
        {"carrinho": carrinho, "itens": cast(Any, carrinho).itens.all()},
    )
