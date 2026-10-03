from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.models import Usuario


class EdicaoUsuarioTests(TestCase):
    usuario: User

    @classmethod
    def setUpTestData(cls) -> None:
        cls.usuario = User.objects.create_user("lucas", email="lucas@example.com")
        User.objects.create_user("outro", email="outro@example.com")

    def test_edicao_exige_login(self) -> None:
        response = self.client.get(reverse("edit_usuario"))
        self.assertRedirects(response, "/login?next=/usuario/edit/")

    def test_edicao_atualiza_conta_e_perfil(self) -> None:
        self.client.force_login(self.usuario)
        response = self.client.post(
            reverse("edit_usuario"),
            {
                "username": "lucas-duarte",
                "email": "lucas@example.com",
                "first_name": "Lucas",
                "last_name": "Duarte",
                "user": self.usuario.pk,
                "aniversario": "2008-10-03",
                "perfil": 1,
            },
        )
        self.assertContains(response, "Dados atualizados com sucesso")
        self.assertTrue(
            User.objects.filter(
                pk=self.usuario.pk, username="lucas-duarte", first_name="Lucas"
            ).exists()
        )
        perfil = Usuario.objects.get(user=self.usuario)
        self.assertEqual(str(perfil.aniversario), "2008-10-03")
        self.assertEqual(perfil.perfil, 2)

    def test_edicao_recusa_email_de_outra_conta(self) -> None:
        self.client.force_login(self.usuario)
        response = self.client.post(
            reverse("edit_usuario"),
            {
                "username": "lucas",
                "email": "outro@example.com",
                "first_name": "",
                "last_name": "",
                "user": self.usuario.pk,
                "aniversario": "",
            },
        )
        self.assertContains(response, "E-mail já usado")
        self.assertTrue(
            User.objects.filter(pk=self.usuario.pk, email="lucas@example.com").exists()
        )
