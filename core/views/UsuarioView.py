from typing import Any, cast

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from core.models import Usuario


def list_usuario_view(request: HttpRequest, id: int | None = None) -> HttpResponse:
    usuarios = cast(Any, Usuario.objects.filter(perfil=2).select_related("user"))

    if id is not None:
        usuarios = usuarios.filter(id=id)

    context = {"usuarios": usuarios}
    return render(
        request,
        template_name="usuario/usuario.html",
        context=context,
        status=200,
    )
