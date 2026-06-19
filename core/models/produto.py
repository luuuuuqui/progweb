from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from django.db import models

from .categoria import Categoria
from .fabricante import Fabricante


class Produto(models.Model):
    nome: models.CharField[str, str] = models.CharField(max_length=100)
    foto: Any = models.ImageField(
        upload_to="fotos/%Y/%m/%d", blank=True, null=True
    )
    destaque: models.BooleanField[bool, bool] = models.BooleanField(default=False)
    promocao: models.BooleanField[bool, bool] = models.BooleanField(default=False)
    msg_promocao: models.CharField[str | None, str | None] = models.CharField(
        max_length=100, blank=True, null=True
    )
    preco: models.DecimalField[Decimal, Decimal] = models.DecimalField(
        max_digits=8, decimal_places=2
    )
    criado_em: models.DateTimeField[datetime, datetime] = models.DateTimeField(
        auto_now_add=True
    )
    alterado_em: models.DateTimeField[datetime, datetime] = models.DateTimeField(
        auto_now=True
    )

    categoria: models.ForeignKey[Categoria | None, Categoria | None] = (
        models.ForeignKey(
            Categoria,
            null=True,
            blank=True,
            related_name="produtos",
            on_delete=models.SET_NULL,
        )
    )

    fabricante: models.ForeignKey[Fabricante | None, Fabricante | None] = (
        models.ForeignKey(
            Fabricante,
            null=True,
            blank=True,
            related_name="produtos",
            on_delete=models.SET_NULL,
        )
    )

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self) -> str:
        return self.nome
