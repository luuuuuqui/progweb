# Django Study Project

Este é um projeto Django criado para fins de aprendizado e testes. É um repositório privado usado como cobaia para experimentar funcionalidades do Django.

## Configuração do Ambiente

1. Clone o repositório:
   ```bash
   git clone <url-do-repo>
   cd django-study
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

## Recuperação de Senha e E-mail

O link "Esqueci minha senha" no login abre `/recovery`. O Django envia uma
mensagem com versões em texto e HTML. O link permite definir e confirmar uma
nova senha, expira em uma hora e é invalidado após a alteração. A resposta da
solicitação não revela se uma conta existe. O campo `Usuario.token` do material
não é necessário: o fluxo usa os tokens nativos do Django.

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

Execute os testes com `python manage.py test`. Eles usam uma caixa de saída em
memória e não enviam mensagens reais.

## Estrutura do Projeto

- `config/`: Configurações do Django
- `core/`: Aplicação principal com modelos, views, etc.
- `templates/`: Templates HTML
- `media/`: Arquivos de mídia (fotos, etc.)
- `requirements.txt`: Dependências Python

## Funcionalidades

- Modelos: Categoria, Fabricante, Produto
- Upload de imagens para produtos
- Interface administrativa do Django

## Notas

Este projeto é usado apenas para aprendizado e não deve ser usado em produção.
