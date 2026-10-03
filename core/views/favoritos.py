from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from core.models import Favorito, Produto


@login_required
def favoritos_view(request: HttpRequest) -> HttpResponse:
    produtos = Produto.objects.filter(favoritos__user=request.user)
    return render(request, "home/favoritos.html", {"produtos": produtos})


@require_POST
def favoritar_view(request: HttpRequest, produto_id: int) -> HttpResponse:
    produto = get_object_or_404(Produto, pk=produto_id)
    destino = "favoritos" if request.POST.get("origem") == "favoritos" else "home"
    if not request.user.is_authenticated:
        request.session["produto_favorito_pendente"] = produto.pk
        return redirect_to_login(reverse(destino))
    favorito, criado = Favorito.objects.get_or_create(
        user=request.user, produto=produto
    )
    if not criado:
        favorito.delete()
    return redirect(destino)
