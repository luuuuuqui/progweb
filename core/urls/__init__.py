from django.urls import path

from core.views import (
    home_view,
    favoritos_view,
    list_produto_view,
    edit_produto_view,
    delete_produto_view,
    create_produto_view,
    details_produto_view,
    
    list_categoria_view,
    create_categoria_view,
    edit_categoria_view,
    delete_categoria_view,
    
    list_fabricante_view,
    create_fabricante_view,
    edit_fabricante_view,
    delete_fabricante_view,
)

urlpatterns = [
    path("", home_view, name='home'),
    path("favoritos/", favoritos_view, name='favoritos'),
    path("produto/", list_produto_view, name='produto'),
    path("produto/<int:id>", list_produto_view, name='produto'),
    path("produto/edit/<int:id>", edit_produto_view, name='edit_produto'),
    path("produto/delete/<int:id>", delete_produto_view, name='delete_produto'),
    path("produto/create/", create_produto_view, name='create_produto'),
    path("produto/details/<int:id>", details_produto_view, name='details_produto'),
    
    # Categoria
    path("categoria/", list_categoria_view, name='categoria'),
    path("categoria/<int:id>", list_categoria_view, name='categoria'),
    path("categoria/edit/<int:id>", edit_categoria_view, name='edit_categoria'),
    path("categoria/delete/<int:id>", delete_categoria_view, name='delete_categoria'),
    path("categoria/create/", create_categoria_view, name='create_categoria'),
    
    # Fabricante
    path("fabricante/", list_fabricante_view, name='fabricante'),
    path("fabricante/<int:id>", list_fabricante_view, name='fabricante'),
    path("fabricante/edit/<int:id>", edit_fabricante_view, name='edit_fabricante'),
    path("fabricante/delete/<int:id>", delete_fabricante_view, name='delete_fabricante'),
    path("fabricante/create/", create_fabricante_view, name='create_fabricante'),
]
