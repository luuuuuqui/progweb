from django.db import models
from .categoria import Categoria
from .fabricante import Fabricante


class Produto(models.Model):
    Produto = models.CharField(null=False, max_length=100)
    foto = models.ImageField(upload_to='fotos/%Y/%m/%d', blank=True)
    destaque = models.BooleanField(default=True)
    promocao = models.BooleanField(default=True)
    msgPromocao = models.CharField(null=True, max_length=100)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.ForeignKey(Categoria, null=True,
    related_name='categoria', on_delete=models.SET_NULL)
    fabricante = models.ForeignKey(Fabricante, null=True,
    related_name='fabricante', on_delete=models.SET_NULL)
