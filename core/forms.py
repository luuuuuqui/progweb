from django import forms

from core.models import Fabricante


class FabricanteForm(forms.ModelForm):  # pyright: ignore[reportMissingTypeArgument]
    class Meta:
        model = Fabricante
        fields = ["nome"]
        widgets = {
            "nome": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Digite o nome do fabricante",
                }
            )
        }
