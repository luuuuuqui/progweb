# Estudos de Programação Web

Repositório de estudos de programação web com Python e Django. O projeto reúne
exercícios e implementações feitas durante o aprendizado, usando uma aplicação
de loja para praticar os recursos do framework.

O objetivo é estudar o desenvolvimento de uma aplicação web: rotas, views,
templates, formulários, persistência de dados, autenticação e integração com
serviços de e-mail. O código evolui conforme novos conteúdos são estudados.

## O que já foi desenvolvido

- Cadastro, listagem, edição e exclusão de produtos, categorias e fabricantes.
- Upload de imagens de produtos e busca por nome no catálogo.
- Registro, login, logout e edição do perfil de usuário.
- Recuperação de senha por e-mail.
- Carrinho com controle de quantidade e confirmação de compra.
- Produtos favoritos vinculados à conta do usuário.
- Administração de dados pelo Django Admin.

## Tecnologias

- Python e Django 6.
- SQLite para persistência local.
- HTML, CSS e templates do Django para a interface.
- Pillow para imagens e python-dotenv para carregar o `.env`.
- Ruff, Pyright e testes do Django para verificar o código.

## Como executar localmente

Use Python 3.12 ou superior, compatível com o Django 6.

1. Clone o repositório:
   ```bash
   git clone https://github.com/luuuuuqui/progweb.git
   cd progweb
   ```

2. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Copie o arquivo de variáveis de ambiente:
   ```bash
   cp .env.example .env
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```
   Preencha `SECRET_KEY` no `.env` com a chave gerada. O arquivo é carregado por
   `python-dotenv`; variáveis definidas no ambiente têm prioridade. Não versione o `.env`.

5. Execute as migrações:
   ```bash
   python manage.py migrate
   ```

6. Crie um superusuário (opcional):
   ```bash
   python manage.py createsuperuser
   ```

7. Execute o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

## Recuperação de senha e e-mail

O link "Esqueci minha senha" no login abre `/recovery`. O Django envia uma
mensagem com versões em texto e HTML. O link permite definir e confirmar uma
nova senha, expira em uma hora e é invalidado após a alteração. A resposta da
solicitação não revela se uma conta existe. O fluxo usa os tokens nativos do Django.

Para enviar pelo Gmail:

1. Ative a verificação em duas etapas e gere uma
   [senha de app](https://support.google.com/accounts/answer/185833?hl=pt-BR),
   caso essa opção esteja disponível para sua conta.
2. Preencha `EMAIL_HOST_USER` com seu Gmail e `EMAIL_HOST_PASSWORD` com a senha
   de app no `.env`. Não use a senha normal da conta.
3. Reinicie o servidor. O projeto usa `smtp.gmail.com`, porta `587` e TLS.

Para testar sem envio real, altere no `.env`:

```dotenv
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

O e-mail e seu link aparecerão no terminal do servidor. Para voltar ao Gmail,
use `django.core.mail.backends.smtp.EmailBackend`. Falhas de envio são
registradas pelo Django no terminal; confira esse registro se a mensagem não
chegar. O domínio e o protocolo do link vêm da requisição; mantenha
`ALLOWED_HOSTS` restrito aos endereços usados pelo projeto.

## Verificações

Com o ambiente virtual ativado:

```bash
python manage.py check
python manage.py test
ruff check .
pyright
```

Os testes de e-mail usam uma caixa de saída em memória e não enviam mensagens reais.

## Estrutura do projeto

- `config/`: Configurações e rotas principais do Django.
- `core/`: Models, formulários, views, rotas, migrations e testes da aplicação.
- `templates/`: Páginas HTML e modelos de e-mail.
- `static/`: Arquivos estáticos, como folhas de estilo.
- `media/`: Imagens enviadas durante o uso, fora do versionamento.
- `.env.example`: Exemplo das variáveis de ambiente necessárias.
- `requirements.txt`: Dependências do projeto.
- `pyproject.toml`: Configurações do Ruff e do Pyright.

Este é um projeto de estudo, sem preparação para uso em produção.
