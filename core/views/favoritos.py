from django.shortcuts import render

from core.models.produto import Produto


def favoritos_view(request):
    ids_str = request.GET.get('ids', '')
    if ids_str:
        # Filter out empty strings and non-numeric values before converting
        ids = [int(id) for id in ids_str.split(',') if id.isdigit()]
        produtos = Produto.objects.filter(id__in=ids)
    else:
        produtos = []
    
    return render(request, "home/favoritos.html", {'produtos': produtos})
