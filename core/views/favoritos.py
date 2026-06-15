from typing import Any, cast

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from core.models.produto import Produto


def favoritos_view(request: HttpRequest) -> HttpResponse:
    ids_str = request.GET.get("ids", "")
    if ids_str:
        # Filter out empty strings and non-numeric values before converting
        ids = [
            int(produto_id)
            for produto_id in ids_str.split(",")
            if produto_id.isdigit()
        ]
        produtos = cast(Any, Produto.objects.filter(id__in=ids))
    else:
        produtos = []

    return render(request, "home/favoritos.html", {"produtos": produtos})
