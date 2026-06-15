from typing import Any, cast

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from core.models.fabricante import Fabricante


def list_fabricante_view(request: HttpRequest) -> HttpResponse:
    fabricantes = cast(Any, Fabricante.objects.all())
    context = {"fabricantes": fabricantes}
    return render(
        request,
        template_name="fabricante/fabricante.html",
        context=context,
        status=200,
    )


def create_fabricante_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        nome = request.POST.get("nome")
        if nome:
            fabricante = Fabricante(nome=nome)
            fabricante.save()
        return redirect("fabricante")

    return render(request, template_name="fabricante/fabricante-edit.html")


def edit_fabricante_view(request: HttpRequest, id: int) -> HttpResponse:
    fabricante = get_object_or_404(Fabricante, id=id)
    if request.method == "POST":
        nome = request.POST.get("nome")
        if nome:
            fabricante.nome = nome
            fabricante.save()
        return redirect("fabricante")

    context = {"fabricante": fabricante}
    return render(
        request,
        template_name="fabricante/fabricante-edit.html",
        context=context,
    )


def delete_fabricante_view(request: HttpRequest, id: int) -> HttpResponse:
    fabricante = get_object_or_404(Fabricante, id=id)
    fabricante.delete()
    return redirect("fabricante")
