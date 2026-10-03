from __future__ import annotations

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from .produto import Produto


class Favorito(models.Model):
    user: models.ForeignKey[User, User] = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="favoritos", on_delete=models.CASCADE
    )
    produto: models.ForeignKey[Produto, Produto] = models.ForeignKey(
        "Produto", related_name="favoritos", on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "produto"], name="favorito_unico_por_usuario"
            )
        ]

    def __str__(self) -> str:
        return str(self.produto)
