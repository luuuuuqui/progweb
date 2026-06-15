from __future__ import annotations

from datetime import datetime

from django.db import models


class Fabricante(models.Model):
    nome: models.CharField[str, str] = models.CharField(max_length=100)
    criado_em: models.DateTimeField[datetime, datetime] = models.DateTimeField(
        auto_now_add=True
    )
    alterado_em: models.DateTimeField[datetime, datetime] = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Fabricante"
        verbose_name_plural = "Fabricantes"

    def __str__(self) -> str:
        return self.nome
