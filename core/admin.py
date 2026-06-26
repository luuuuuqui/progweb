from django.contrib import admin

from .models import Categoria, Fabricante, Produto, Usuario

admin.site.register(Fabricante)
admin.site.register(Categoria)
admin.site.register(Produto)
admin.site.register(Usuario)
