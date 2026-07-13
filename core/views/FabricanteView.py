from typing import Any, cast

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core.forms import FabricanteForm
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
        form = FabricanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("fabricante")
    else:
        form = FabricanteForm()

    return render(
        request,
        template_name="fabricante/fabricante-edit.html",
        context={"form": form},
    )


def edit_fabricante_view(request: HttpRequest, id: int) -> HttpResponse:
    fabricante = get_object_or_404(Fabricante, id=id)
    if request.method == "POST":
        form = FabricanteForm(request.POST, instance=fabricante)
        if form.is_valid():
            form.save()
            return redirect("fabricante")
    else:
        form = FabricanteForm(instance=fabricante)

    context = {"fabricante": fabricante, "form": form}
    return render(
        request,
        template_name="fabricante/fabricante-edit.html",
        context=context,
    )


@require_POST
def delete_fabricante_view(request: HttpRequest, id: int) -> HttpResponse:
    fabricante = get_object_or_404(Fabricante, id=id)
    fabricante.delete()
    return redirect("fabricante")
