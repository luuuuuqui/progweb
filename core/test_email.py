import re
from datetime import timedelta
from typing import cast
from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="suporte@example.com",
)
class RecuperacaoSenhaTests(TestCase):
    usuario: User

    def setUp(self) -> None:
        self.usuario = User.objects.create_user(
            "lucas", email="lucas@example.com", password="senha-antiga"
        )

    def test_fluxo_completo_envia_email_e_invalida_link(self) -> None:
        self.assertContains(self.client.get(reverse("login")), "Esqueci minha senha")
        response = self.client.post(reverse("recovery"), {"email": "lucas@example.com"})
        self.assertRedirects(response, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        email = cast(EmailMultiAlternatives, mail.outbox[0])
        self.assertEqual(email.to, ["lucas@example.com"])
        self.assertEqual(email.from_email, "suporte@example.com")
        self.assertEqual(email.alternatives[0][1], "text/html")
        link = re.search(r"http://testserver(/change-password/\S+)", str(email.body))
        assert link is not None
        path = link.group(1)
        response = self.client.get(path)
        confirmacao = response.headers["Location"]
        self.assertContains(self.client.get(confirmacao), "Alterar senha")
        response = self.client.post(
            confirmacao,
            {
                "new_password1": "Nova-senha-segura-843!",
                "new_password2": "Nova-senha-segura-843!",
            },
        )
        self.assertRedirects(response, reverse("password_reset_complete"))
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password("Nova-senha-segura-843!"))
        self.assertFalse(self.usuario.check_password("senha-antiga"))
        self.assertContains(Client().get(path), "inválido ou expirou")

    def test_email_desconhecido_nao_revela_contas(self) -> None:
        response = self.client.post(
            reverse("recovery"), {"email": "ausente@example.com"}
        )
        self.assertRedirects(response, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 0)

    def test_email_invalido_e_csrf(self) -> None:
        response = self.client.post(reverse("recovery"), {"email": "invalido"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)
        response = Client(enforce_csrf_checks=True).post(
            reverse("recovery"), {"email": "lucas@example.com"}
        )
        self.assertEqual(response.status_code, 403)

    def test_token_expira_e_senha_fraca_e_recusada(self) -> None:
        token = default_token_generator.make_token(self.usuario)
        path = reverse(
            "password_reset_confirm",
            kwargs={
                "uidb64": urlsafe_base64_encode(force_bytes(self.usuario.pk)),
                "token": token,
            },
        )
        with patch.object(
            default_token_generator,
            "_now",
            return_value=timezone.now().replace(tzinfo=None) + timedelta(hours=2),
        ):
            self.assertContains(self.client.get(path), "inválido ou expirou")
        response = self.client.get(path)
        response = self.client.post(
            response.headers["Location"],
            {"new_password1": "123", "new_password2": "123"},
        )
        self.assertEqual(response.status_code, 200)
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password("senha-antiga"))
