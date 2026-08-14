
from .auth import *

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
from .favoritos import favoritos_view
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
    'home_view',
    'favoritos_view',
    'list_produto_view',
    'edit_produto_view',
    'delete_produto_view',
    'create_produto_view',
    'details_produto_view',

    'list_categoria_view',
    'create_categoria_view',
    'edit_categoria_view',
    'delete_categoria_view',

    'list_fabricante_view',
    'create_fabricante_view',
    'edit_fabricante_view',
    'delete_fabricante_view',

    'list_usuario_view',
    'edit_usuario_view',

    'login_view',
    'register_view',
]
