# estudos de programação web

repositório de estudos de programação web com python e django. o projeto reúne
exercícios e implementações feitas durante o aprendizado, usando uma aplicação
de loja para praticar os recursos do framework.

o objetivo é estudar o desenvolvimento de uma aplicação web: rotas, views,
templates, formulários, persistência de dados, autenticação e integração com
serviços de e-mail. o código evolui conforme novos conteúdos são estudados.

## o que já foi desenvolvido

- cadastro, listagem, edição e exclusão de produtos, categorias e fabricantes.
- upload de imagens de produtos e busca por nome no catálogo.
- registro, login, logout e edição do perfil de usuário.
- recuperação de senha por e-mail.
- carrinho com controle de quantidade e confirmação de compra.
- produtos favoritos vinculados à conta do usuário.
- administração de dados pelo django admin.

## tecnologias

- python e django 6.
- sqlite para persistência local.
- html, css e templates do django para a interface.
- pillow para imagens e python-dotenv para carregar o `.env`.
- ruff, pyright e testes do django para verificar o código.

## como executar localmente

use python 3.12 ou superior, compatível com o django 6.

1. clone o repositório:
   ```bash
   git clone https://github.com/luuuuuqui/progweb.git
   cd progweb
   ```

2. crie um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # no windows: .venv\Scripts\activate
   ```

3. instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. copie o arquivo de variáveis de ambiente:
   ```bash
   cp .env.example .env
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```
   preencha `SECRET_KEY` no `.env` com a chave gerada. o arquivo é carregado por
   `python-dotenv`; variáveis definidas no ambiente têm prioridade. não versione o `.env`.

5. execute as migrações:
   ```bash
   python manage.py migrate
   ```

6. crie um superusuário (opcional):
   ```bash
   python manage.py createsuperuser
   ```

7. execute o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

## recuperação de senha e e-mail

o link "esqueci minha senha" no login abre `/recovery`. o django envia uma
mensagem com versões em texto e html. o link permite definir e confirmar uma
nova senha, expira em uma hora e é invalidado após a alteração. a resposta da
solicitação não revela se uma conta existe. o fluxo usa os tokens nativos do django.

para enviar pelo gmail:

1. ative a verificação em duas etapas e gere uma
   [senha de app](https://support.google.com/accounts/answer/185833?hl=pt-BR),
   caso essa opção esteja disponível para sua conta.
2. preencha `EMAIL_HOST_USER` com seu gmail e `EMAIL_HOST_PASSWORD` com a senha
   de app no `.env`. não use a senha normal da conta.
3. reinicie o servidor. o projeto usa `smtp.gmail.com`, porta `587` e tls.

para testar sem envio real, altere no `.env`:

```dotenv
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

o e-mail e seu link aparecerão no terminal do servidor. para voltar ao gmail,
use `django.core.mail.backends.smtp.EmailBackend`. falhas de envio são
registradas pelo django no terminal; confira esse registro se a mensagem não
chegar. o domínio e o protocolo do link vêm da requisição; mantenha
`ALLOWED_HOSTS` restrito aos endereços usados pelo projeto.

## verificações

com o ambiente virtual ativado:

```bash
python manage.py check
python manage.py test
ruff check .
pyright
```

os testes de e-mail usam uma caixa de saída em memória e não enviam mensagens reais.

## estrutura do projeto

- `config/`: configurações e rotas principais do django.
- `core/`: models, formulários, views, rotas, migrations e testes da aplicação.
- `templates/`: páginas html e modelos de e-mail.
- `static/`: arquivos estáticos, como folhas de estilo.
- `media/`: imagens enviadas durante o uso, fora do versionamento.
- `.env.example`: exemplo das variáveis de ambiente necessárias.
- `requirements.txt`: dependências do projeto.
- `pyproject.toml`: configurações do ruff e do pyright.

este é um projeto de estudo, sem preparação para uso em produção.
