from typing import Any, cast

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from core.models.produto import Produto


def home_view(request: HttpRequest) -> HttpResponse:
    produto = request.GET.get("produto")
    produtos = cast(Any, Produto.objects.all())
    if produto is not None:
        produtos = produtos.filter(nome__contains=produto)

    context = {"produtos": produtos}
    return render(request, template_name="home/home.html", context=context, status=200)
