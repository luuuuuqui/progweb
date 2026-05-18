from django.http import HttpResponse
from datetime import timedelta
from django.utils import timezone

# 1. A sua importação adaptada (substitua 'produto' pelo nome real do seu arquivo)
from core.models.produto import Produto

def list_produto_view(request):
    # Capturando os parâmetros da URL
    produto = request.GET.get("produto")
    categoria = request.GET.get("categoria")
    dias = request.GET.get("dias")
    
    # 2. Comando para pegar todos os produtos do banco
    produtos = Produto.objects.all()
    
    # 3. Aplicando os filtros ensinados no PDF
    if produto is not None:
        # Filtro por aproximação de texto (like)
        produtos = produtos.filter(nome__contains=produto)
        
    if categoria is not None:
        # Filtro por chave estrangeira
        produtos = produtos.filter(categoria__nome=categoria)
        
    if dias is not None:
        # Filtro de datas (maior ou igual a X dias atrás)
        now = timezone.now()
        now = now - timedelta(days=int(dias))
        produtos = produtos.filter(criado_em__gte=now)
    
    # Imprime no terminal onde o servidor está rodando
    print(produtos)
    
    return HttpResponse('<h1>Consulta realizada! Veja o terminal.</h1>')