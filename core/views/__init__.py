from .auth import login_view, logout_view, register_view
from .CarrinhoView import (
    alterar_quantidade_view,
    carrinho_confirmado_view,
    confirmar_carrinho_view,
    create_carrinhoitem_view,
    list_carrinho_view,
    remover_item_view,
)
from .CategoriaView import (
    create_categoria_view,
    delete_categoria_view,
    edit_categoria_view,
    list_categoria_view,
)
from .FabricanteView import (
    create_fabricante_view,
    delete_fabricante_view,
    edit_fabricante_view,
    list_fabricante_view,
)
from .favoritos import favoritar_view, favoritos_view
from .home import home_view
from .ProdutoView import (
    create_produto_view,
    delete_produto_view,
    details_produto_view,
    edit_produto_view,
    list_produto_view,
)
from .UsuarioView import edit_usuario_view, list_usuario_view

__all__ = [
    "home_view",
    "favoritos_view",
    "favoritar_view",
    "create_carrinhoitem_view",
    "list_carrinho_view",
    "alterar_quantidade_view",
    "remover_item_view",
    "confirmar_carrinho_view",
    "carrinho_confirmado_view",
    "list_produto_view",
    "edit_produto_view",
    "delete_produto_view",
    "create_produto_view",
    "details_produto_view",
    "list_categoria_view",
    "create_categoria_view",
    "edit_categoria_view",
    "delete_categoria_view",
    "list_fabricante_view",
    "create_fabricante_view",
    "edit_fabricante_view",
    "delete_fabricante_view",
    "list_usuario_view",
    "edit_usuario_view",
    "login_view",
    "logout_view",
    "register_view",
]
