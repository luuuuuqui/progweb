from typing import Any, cast

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from core.forms import UserForm, UserUsuarioForm
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


@login_required
def edit_usuario_view(request: HttpRequest) -> HttpResponse:
    usuario = get_object_or_404(Usuario, user=request.user)
    message: dict[str, str] | None = None
    email_unused = True

    if request.method == "POST":
        usuarioForm = UserUsuarioForm(request.POST, instance=usuario)
        userForm = UserForm(request.POST, instance=usuario.user)

        verify_email = (
            Usuario.objects.filter(user__email=request.POST.get("email", ""))
            .exclude(user=usuario.user)
            .first()
        )
        email_unused = verify_email is None

        if usuarioForm.is_valid() and userForm.is_valid() and email_unused:
            usuarioForm.save()
            userForm.save()
            message = {"type": "success", "text": "Dados atualizados com sucesso"}
        else:
            if request.method == "POST":
                if email_unused:
                    message = {"type": "danger", "text": "Dados inválidos"}
                else:
                    message = {"type": "warning", "text": "E-mail já usado"}
    else:
        usuarioForm = UserUsuarioForm(instance=usuario)
        userForm = UserForm(instance=usuario.user)

    context = {
        "usuarioForm": usuarioForm,
        "userForm": userForm,
        "message": message,
    }
    return render(
        request,
        template_name="usuario/usuario-edit.html",
        context=context,
        status=200,
    )
