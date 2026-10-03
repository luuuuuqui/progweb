from django.contrib import admin

from .models import (
    Carrinho,
    CarrinhoItem,
    Categoria,
    Fabricante,
    Favorito,
    Produto,
    Usuario,
)

admin.site.register(Fabricante)
admin.site.register(Categoria)
admin.site.register(Produto)
admin.site.register(Usuario)
admin.site.register(Carrinho)
admin.site.register(CarrinhoItem)
admin.site.register(Favorito)
