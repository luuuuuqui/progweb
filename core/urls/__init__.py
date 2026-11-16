from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from core.views import (
    alterar_quantidade_view,
    carrinho_confirmado_view,
    confirmar_carrinho_view,
    create_carrinhoitem_view,
    create_categoria_view,
    create_fabricante_view,
    create_produto_view,
    delete_categoria_view,
    delete_fabricante_view,
    delete_produto_view,
    details_produto_view,
    edit_categoria_view,
    edit_fabricante_view,
    edit_produto_view,
    edit_usuario_view,
    favoritar_view,
    favoritos_view,
    home_view,
    list_carrinho_view,
    list_categoria_view,
    list_fabricante_view,
    list_produto_view,
    list_usuario_view,
    login_view,
    logout_view,
    register_view,
    remover_item_view,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("favoritos/", favoritos_view, name="favoritos"),
    path("favoritos/<int:produto_id>/", favoritar_view, name="favoritar_produto"),
    path("carrinho/", list_carrinho_view, name="list_carrinho"),
    path(
        "carrinho/<int:produto_id>/",
        create_carrinhoitem_view,
        name="create_carrinhoitem",
    ),
    path("carrinho/confirmar/", confirmar_carrinho_view, name="confirmar_carrinho"),
    path(
        "carrinho/confirmado/<int:carrinho_id>/",
        carrinho_confirmado_view,
        name="carrinho_confirmado",
    ),
    path(
        "carrinho/adicionar/<int:item_id>/",
        alterar_quantidade_view,
        {"acao": "adicionar"},
        name="adicionar_carrinhoitem",
    ),
    path(
        "carrinho/diminuir/<int:item_id>/",
        alterar_quantidade_view,
        {"acao": "diminuir"},
        name="diminuir_carrinhoitem",
    ),
    path(
        "carrinho/remover/<int:item_id>/",
        remover_item_view,
        name="remover_carrinhoitem",
    ),
    path("produto/", list_produto_view, name="produto"),
    path("produto/<int:id>", list_produto_view, name="produto"),
    path("produto/edit/<int:id>", edit_produto_view, name="edit_produto"),
    path("produto/delete/<int:id>", delete_produto_view, name="delete_produto"),
    path("produto/create/", create_produto_view, name="create_produto"),
    path("produto/details/<int:id>", details_produto_view, name="details_produto"),
    # Categoria
    path("categoria/", list_categoria_view, name="categoria"),
    path("categoria/<int:id>", list_categoria_view, name="categoria"),
    path("categoria/edit/<int:id>", edit_categoria_view, name="edit_categoria"),
    path("categoria/delete/<int:id>", delete_categoria_view, name="delete_categoria"),
    path("categoria/create/", create_categoria_view, name="create_categoria"),
    # Fabricante
    path("fabricante/", list_fabricante_view, name="fabricante"),
    path("fabricante/<int:id>", list_fabricante_view, name="fabricante"),
    path("fabricante/edit/<int:id>", edit_fabricante_view, name="edit_fabricante"),
    path(
        "fabricante/delete/<int:id>",
        delete_fabricante_view,
        name="delete_fabricante",
    ),
    path("fabricante/create/", create_fabricante_view, name="create_fabricante"),
    # Usuario
    path("usuario/", list_usuario_view, name="usuario"),
    path("usuario/<int:id>", list_usuario_view, name="usuario"),
    path("usuario/edit/", edit_usuario_view, name="edit_usuario"),
    # Recuperação de senha
    path(
        "recovery",
        auth_views.PasswordResetView.as_view(
            template_name="auth/password-reset.html",
            email_template_name="auth/recovery.txt",
            html_email_template_name="auth/recovery.html",
            subject_template_name="auth/recovery-subject.txt",
            success_url=reverse_lazy("password_reset_done"),
            extra_context={"title": "Recuperar senha", "button_text": "Recuperar"},
        ),
        name="recovery",
    ),
    path(
        "recovery/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth/password-reset.html",
            extra_context={
                "title": "Recuperar senha",
                "notice": "Se o e-mail estiver cadastrado em uma conta ativa, "
                "você receberá um link para recuperar a senha.",
            },
        ),
        name="password_reset_done",
    ),
    path(
        "change-password/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth/password-reset.html",
            success_url=reverse_lazy("password_reset_complete"),
            extra_context={"title": "Alterar senha", "button_text": "Alterar"},
        ),
        name="password_reset_confirm",
    ),
    path(
        "change-password/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth/password-reset.html",
            extra_context={
                "title": "Alterar senha",
                "notice": "Senha alterada com sucesso! Entre com sua nova senha.",
            },
        ),
        name="password_reset_complete",
    ),
    # login
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("register", register_view, name="register"),
]
