from urllib.parse import urlencode

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from core.forms import LoginForm, RegisterForm
from core.models import Favorito, Produto


def _destino_apos_login(request: HttpRequest) -> str:
    destino = request.POST.get("next") or request.GET.get("next") or reverse("home")
    if url_has_allowed_host_and_scheme(
        destino, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return destino
    return reverse("home")


def login_view(request: HttpRequest) -> HttpResponse:
    loginForm = LoginForm()
    message = None
    destino = _destino_apos_login(request)

    if request.user.is_authenticated:
        return redirect(destino)

    if request.method == "POST":
        loginForm = LoginForm(request.POST)

        if loginForm.is_valid():
            user = authenticate(
                request,
                username=loginForm.cleaned_data["username"],
                password=loginForm.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                produto_id = request.session.pop("produto_favorito_pendente", None)
                if isinstance(produto_id, int):
                    produto = Produto.objects.filter(pk=produto_id).first()
                    if produto is not None:
                        Favorito.objects.get_or_create(user=user, produto=produto)
                return redirect(destino)
            else:
                message = {"type": "danger", "text": "Dados de usuário incorretos"}

    context = {
        "form": loginForm,
        "message": message,
        "title": "Login",
        "button_text": "Entrar",
        "link_text": "Registrar",
        "link_href": reverse("register") + "?" + urlencode({"next": destino}),
        "next": destino,
    }
    return render(request, template_name="auth/auth.html", context=context, status=200)


def register_view(request: HttpRequest) -> HttpResponse:
    registerForm = RegisterForm()
    message = None
    destino = _destino_apos_login(request)

    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        registerForm = RegisterForm(request.POST)

        if registerForm.is_valid():
            username = registerForm.cleaned_data["username"]
            email = registerForm.cleaned_data["email"]
            password = registerForm.cleaned_data["password"]
            verifyUsername = User.objects.filter(username=username).first()
            verifyEmail = User.objects.filter(email=email).first()

            if verifyUsername is not None:
                message = {
                    "type": "danger",
                    "text": "Já existe um usuário com este username!",
                }
            elif verifyEmail is not None:
                message = {
                    "type": "danger",
                    "text": "Já existe um usuário com este e-mail!",
                }
            else:
                User.objects.create_user(username, email, password)
                message = {"type": "success", "text": "Conta criada com sucesso!"}

    context = {
        "form": registerForm,
        "message": message,
        "title": "Registrar",
        "button_text": "Registrar",
        "link_text": "Login",
        "link_href": reverse("login") + "?" + urlencode({"next": destino}),
        "next": destino,
    }
    return render(request, template_name="auth/auth.html", context=context, status=200)


@require_POST
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("home")
