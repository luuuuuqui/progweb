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
