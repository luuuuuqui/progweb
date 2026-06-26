from __future__ import annotations

from datetime import date, datetime
from typing import Any, cast

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

PERFIL = (
    (1, "Admin"),
    (2, "Usuario"),
)


class Usuario(models.Model):
    user: models.OneToOneField[User, User] = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    perfil: models.IntegerField[int, int] = models.IntegerField(
        choices=PERFIL,
        default=2,
    )
    aniversario: models.DateField[date | None, date | None] = models.DateField(
        default=None,
        null=True,
        blank=True,
    )
    criado_em: models.DateTimeField[datetime, datetime] = models.DateTimeField(
        auto_now_add=True,
    )
    alterado_em: models.DateTimeField[datetime, datetime] = models.DateTimeField(
        auto_now=True,
    )
    token: models.CharField[str | None, str | None] = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self) -> str:
        return cast(str, cast(Any, self.user).username)


@receiver(post_save, sender=User)
def create_user_usuario(
    sender: type[User],
    instance: User,
    created: bool,
    **kwargs: Any,
) -> None:
    if created:
        Usuario.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_usuario(
    sender: type[User],
    instance: User,
    **kwargs: Any,
) -> None:
    try:
        cast(Any, instance).usuario.save()
    except Usuario.DoesNotExist:
        Usuario.objects.create(user=instance)
