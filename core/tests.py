from decimal import Decimal

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from core.models import Carrinho, CarrinhoItem, Favorito, Produto, Usuario


class LojaTests(TestCase):
    usuario: User
    outro_usuario: User
    produto: Produto
    outro_produto: Produto

    @classmethod
    def setUpTestData(cls) -> None:
        cls.usuario = User.objects.create_user("lucas", password="senha-de-teste")
        cls.outro_usuario = User.objects.create_user("outro", password="outra-senha")
        cls.produto = Produto.objects.create(nome="Teclado", preco=Decimal("19.90"))
        cls.outro_produto = Produto.objects.create(nome="Mouse", preco=Decimal("10.00"))

    def comprar(self, produto: Produto | None = None) -> CarrinhoItem:
        produto = produto or self.produto
        response = self.client.post(reverse("create_carrinhoitem", args=[produto.pk]))
        self.assertRedirects(response, reverse("list_carrinho"))
        return CarrinhoItem.objects.get(
            carrinho_id=self.client.session["carrinho_id"], produto=produto
        )

    def confirmar(self) -> Carrinho:
        item = self.comprar()
        self.client.force_login(self.usuario)
        response = self.client.post(reverse("confirmar_carrinho"))
        self.assertRedirects(
            response, reverse("carrinho_confirmado", args=[item.carrinho.pk])
        )
        return Carrinho.objects.get(pk=item.carrinho.pk)

    def test_home_tem_compra_preco_e_favoritos(self) -> None:
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Comprar")
        self.assertContains(response, "19.90")
        self.assertContains(response, reverse("favoritos"))
        self.assertContains(response, reverse("list_carrinho"))

    def test_carrinho_vazio_nao_cria_pedido(self) -> None:
        response = self.client.get(reverse("list_carrinho"))
        self.assertContains(response, "Seu carrinho está vazio.")
        self.assertEqual(Carrinho.objects.count(), 0)

    def test_compra_anonima_agrupa_itens_e_calcula_totais(self) -> None:
        item = self.comprar()
        self.comprar()
        self.comprar(self.outro_produto)
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 2)
        self.assertEqual(item.total, Decimal("39.80"))
        self.assertEqual(item.carrinho.total, Decimal("49.80"))
        self.assertEqual(CarrinhoItem.objects.count(), 2)
        self.assertIsNone(item.carrinho.user)

    def test_carrinhos_sao_separados_por_sessao(self) -> None:
        item = self.comprar()
        outro_cliente = Client()
        outro_cliente.post(reverse("create_carrinhoitem", args=[self.produto.pk]))
        self.assertNotEqual(outro_cliente.session["carrinho_id"], item.carrinho.pk)

    def test_sessao_com_carrinho_removido_cria_outro(self) -> None:
        item = self.comprar()
        carrinho_id = item.carrinho.pk
        item.carrinho.delete()
        novo_item = self.comprar()
        self.assertNotEqual(novo_item.carrinho.pk, carrinho_id)

    def test_controles_de_quantidade_e_remocao(self) -> None:
        item = self.comprar()
        self.client.post(reverse("adicionar_carrinhoitem", args=[item.pk]))
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 2)
        self.client.post(reverse("diminuir_carrinhoitem", args=[item.pk]))
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 1)
        self.client.post(reverse("diminuir_carrinhoitem", args=[item.pk]))
        self.assertFalse(CarrinhoItem.objects.filter(pk=item.pk).exists())
        novo_item = self.comprar()
        self.client.post(reverse("remover_carrinhoitem", args=[novo_item.pk]))
        self.assertFalse(CarrinhoItem.objects.exists())

    def test_nao_altera_itens_de_outra_sessao(self) -> None:
        item = self.comprar()
        outro_cliente = Client()
        outro_cliente.post(reverse("create_carrinhoitem", args=[self.outro_produto.pk]))
        for rota in (
            "adicionar_carrinhoitem",
            "diminuir_carrinhoitem",
            "remover_carrinhoitem",
        ):
            response = outro_cliente.post(reverse(rota, args=[item.pk]))
            self.assertEqual(response.status_code, 404)
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 1)

    def test_alteracoes_exigem_post_e_csrf(self) -> None:
        item = self.comprar()
        for rota, identificador in (
            ("create_carrinhoitem", self.produto.pk),
            ("adicionar_carrinhoitem", item.pk),
            ("diminuir_carrinhoitem", item.pk),
            ("remover_carrinhoitem", item.pk),
            ("favoritar_produto", self.produto.pk),
        ):
            response = self.client.get(reverse(rota, args=[identificador]))
            self.assertEqual(response.status_code, 405)
            response = Client(enforce_csrf_checks=True).post(
                reverse(rota, args=[identificador])
            )
            self.assertEqual(response.status_code, 403)

    def test_login_preserva_carrinho_e_retorna_a_confirmacao(self) -> None:
        item = self.comprar()
        response = self.client.post(reverse("confirmar_carrinho"))
        self.assertRedirects(response, "/login?next=/carrinho/confirmar/")
        response = self.client.post(
            reverse("login"),
            {
                "username": "lucas",
                "password": "senha-de-teste",
                "next": reverse("confirmar_carrinho"),
            },
        )
        self.assertRedirects(response, reverse("confirmar_carrinho"))
        self.assertEqual(self.client.session["carrinho_id"], item.carrinho.pk)
        item.carrinho.refresh_from_db()
        self.assertEqual(item.carrinho.situacao, Carrinho.ABERTO)
        response = self.client.post(reverse("confirmar_carrinho"))
        self.assertRedirects(
            response, reverse("carrinho_confirmado", args=[item.carrinho.pk])
        )

    def test_confirmacao_associa_user_e_mostra_itens(self) -> None:
        # os ids do perfil e da conta podem ser diferentes.
        Usuario.objects.filter(user=self.usuario).delete()
        perfil = Usuario.objects.create(user=self.usuario)
        self.assertNotEqual(perfil.pk, self.usuario.pk)
        carrinho = self.confirmar()
        self.assertEqual(carrinho.user, self.usuario)
        self.assertEqual(carrinho.situacao, Carrinho.CONFIRMADO)
        self.assertIsNotNone(carrinho.confirmado_em)
        self.assertNotIn("carrinho_id", self.client.session)
        response = self.client.get(reverse("carrinho_confirmado", args=[carrinho.pk]))
        self.assertContains(response, "Compra confirmada")
        self.assertContains(response, "Teclado")
        self.assertContains(response, "19.90")

    def test_get_de_confirmacao_nao_finaliza(self) -> None:
        item = self.comprar()
        self.client.force_login(self.usuario)
        response = self.client.get(reverse("confirmar_carrinho"))
        self.assertEqual(response.status_code, 200)
        item.carrinho.refresh_from_db()
        self.assertEqual(item.carrinho.situacao, Carrinho.ABERTO)
        self.assertIsNone(item.carrinho.confirmado_em)

    def test_carrinho_vazio_nao_pode_ser_confirmado(self) -> None:
        item = self.comprar()
        self.client.post(reverse("remover_carrinhoitem", args=[item.pk]))
        self.client.force_login(self.usuario)
        response = self.client.post(reverse("confirmar_carrinho"))
        self.assertRedirects(response, reverse("list_carrinho"))
        item.carrinho.refresh_from_db()
        self.assertEqual(item.carrinho.situacao, Carrinho.ABERTO)

    def test_pedido_confirmado_nao_e_reutilizado(self) -> None:
        carrinho = self.confirmar()
        session = self.client.session
        session["carrinho_id"] = carrinho.pk
        session.save()
        item = CarrinhoItem.objects.get(carrinho=carrinho)
        self.client.post(reverse("adicionar_carrinhoitem", args=[item.pk]))
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 1)
        novo_item = self.comprar()
        self.assertNotEqual(novo_item.carrinho.pk, carrinho.pk)

    def test_recibo_so_pode_ser_visto_pelo_dono(self) -> None:
        carrinho = self.confirmar()
        self.client.force_login(self.outro_usuario)
        response = self.client.get(reverse("carrinho_confirmado", args=[carrinho.pk]))
        self.assertEqual(response.status_code, 404)

    def test_pedido_preserva_nome_e_preco_originais(self) -> None:
        carrinho = self.confirmar()
        self.produto.nome = "Outro teclado"
        self.produto.preco = Decimal("50.00")
        self.produto.save()
        self.produto.delete()
        response = self.client.get(reverse("carrinho_confirmado", args=[carrinho.pk]))
        self.assertContains(response, "Teclado")
        self.assertNotContains(response, "Outro teclado")
        self.assertEqual(carrinho.total, Decimal("19.90"))

    def test_produto_removido_impede_confirmacao(self) -> None:
        item = self.comprar()
        self.produto.delete()
        self.client.force_login(self.usuario)
        response = self.client.post(reverse("confirmar_carrinho"))
        self.assertRedirects(response, reverse("list_carrinho"))
        self.assertFalse(Carrinho.objects.filter(situacao=Carrinho.CONFIRMADO).exists())
        self.client.post(reverse("adicionar_carrinhoitem", args=[item.pk]))
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 1)

    def test_favoritar_anonimo_solicita_login_e_salva_apos_entrar(self) -> None:
        response = self.client.post(
            reverse("favoritar_produto", args=[self.produto.pk])
        )
        self.assertRedirects(response, "/login?next=/")
        self.assertFalse(Favorito.objects.exists())
        self.client.post(reverse("login"), {"username": "lucas", "password": "errada"})
        self.assertFalse(Favorito.objects.exists())
        response = self.client.post(
            reverse("login"), {"username": "lucas", "password": "senha-de-teste"}
        )
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(
            Favorito.objects.filter(user=self.usuario, produto=self.produto).exists()
        )
        self.assertNotIn("produto_favorito_pendente", self.client.session)
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Favoritado")

    def test_favoritos_persistem_por_usuario_e_ignoram_ids_da_url(self) -> None:
        self.client.force_login(self.usuario)
        self.client.post(reverse("favoritar_produto", args=[self.produto.pk]))
        outro_cliente = Client()
        outro_cliente.force_login(self.usuario)
        response = outro_cliente.get(reverse("favoritos"))
        self.assertContains(response, "Teclado")
        self.client.force_login(self.outro_usuario)
        self.client.post(reverse("favoritar_produto", args=[self.outro_produto.pk]))
        response = self.client.get(reverse("favoritos"), {"ids": self.produto.pk})
        self.assertContains(response, "Mouse")
        self.assertNotContains(response, "Teclado")

    def test_remover_favorito_atualiza_listagem(self) -> None:
        self.client.force_login(self.usuario)
        self.client.post(reverse("favoritar_produto", args=[self.produto.pk]))
        response = self.client.post(
            reverse("favoritar_produto", args=[self.produto.pk]),
            {"origem": "favoritos"},
        )
        self.assertRedirects(response, reverse("favoritos"))
        self.assertFalse(Favorito.objects.filter(user=self.usuario).exists())
        self.assertContains(
            self.client.get(reverse("favoritos")), "nenhum produto favoritado"
        )

    def test_listagem_de_favoritos_exige_login(self) -> None:
        response = self.client.get(reverse("favoritos"))
        self.assertRedirects(response, "/login?next=/favoritos/")

    def test_login_bloqueia_redirecionamento_externo(self) -> None:
        response = self.client.post(
            reverse("login"),
            {
                "username": "lucas",
                "password": "senha-de-teste",
                "next": "https://example.com/",
            },
        )
        self.assertRedirects(response, reverse("home"))

    def test_logout_permite_trocar_de_conta(self) -> None:
        self.client.force_login(self.usuario)
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("home"))
        self.assertNotIn("_auth_user_id", self.client.session)
