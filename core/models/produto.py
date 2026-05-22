from django.db import models
from .categoria import Categoria
from .fabricante import Fabricante

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='fotos/%Y/%m/%d', blank=True, null=True)
    destaque = models.BooleanField(default=False) # Mudei para False por padrão (mais seguro)
    promocao = models.BooleanField(default=False) # Mudei para False por padrão
    msg_promocao = models.CharField(max_length=100, blank=True, null=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    
    categoria = models.ForeignKey(
        Categoria, 
        null=True,
        blank=True, # Adicionado para permitir salvar sem categoria no painel
        related_name='produtos', # Busca reversa no plural
        on_delete=models.SET_NULL
    )
    
    fabricante = models.ForeignKey(
        Fabricante, 
        null=True,
        blank=True,
        related_name='produtos', 
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome