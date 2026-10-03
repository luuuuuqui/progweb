from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, cast

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from .produto import Produto


class Carrinho(models.Model):
    ABERTO = 0
    CONFIRMADO = 1

    criado_em: models.DateTimeField[datetime, datetime] = models.DateTimeField(
        auto_now_add=True
    )
    user: models.ForeignKey[User | None, User | None] = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="carrinhos",
        on_delete=models.SET_NULL,
    )
    situacao: models.PositiveIntegerField[int, int] = models.PositiveIntegerField(
        default=ABERTO, choices=((ABERTO, "Aberto"), (CONFIRMADO, "Confirmado"))
    )
    confirmado_em: models.DateTimeField[datetime | None, datetime | None] = (
        models.DateTimeField(null=True, blank=True)
    )
    user_id: int | None

    @property
    def total(self) -> Decimal:
        return sum(
            (item.total for item in cast(Any, self).itens.all()), Decimal("0.00")
        )

    def __str__(self) -> str:
        return f"Carrinho {self.pk}"


class CarrinhoItem(models.Model):
    criado_em: models.DateTimeField[datetime, datetime] = models.DateTimeField(
        auto_now_add=True
    )
    carrinho: models.ForeignKey[Carrinho, Carrinho] = models.ForeignKey(
        Carrinho, related_name="itens", on_delete=models.CASCADE
    )
    produto: models.ForeignKey[Produto | None, Produto | None] = models.ForeignKey(
        "Produto",
        null=True,
        blank=True,
        related_name="carrinhos",
        on_delete=models.SET_NULL,
    )
    nome_produto: models.CharField[str, str] = models.CharField(max_length=100)
    quantidade: models.PositiveIntegerField[int, int] = models.PositiveIntegerField(
        default=1
    )
    preco: models.DecimalField[Decimal, Decimal] = models.DecimalField(
        max_digits=8, decimal_places=2
    )
    produto_id: int | None

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["carrinho", "produto"], name="produto_unico_no_carrinho"
            ),
            models.CheckConstraint(
                condition=models.Q(quantidade__gte=1), name="quantidade_item_positiva"
            ),
        ]

    @property
    def total(self) -> Decimal:
        return self.quantidade * self.preco

    def __str__(self) -> str:
        return self.nome_produto
