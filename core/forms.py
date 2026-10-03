from typing import TYPE_CHECKING, Any

from django import forms
from django.contrib.auth.models import User

from core.models import Fabricante, Usuario

# ModelForm é genérico nos stubs, mas não aceita subscrição em execução.
if TYPE_CHECKING:
    _FabricanteModelForm = forms.ModelForm[Fabricante]
    _UserModelForm = forms.ModelForm[User]
    _UsuarioModelForm = forms.ModelForm[Usuario]
else:
    _FabricanteModelForm = forms.ModelForm
    _UserModelForm = forms.ModelForm
    _UsuarioModelForm = forms.ModelForm


class FabricanteForm(_FabricanteModelForm):
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


class UserForm(_UserModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }


class UserUsuarioForm(_UsuarioModelForm):
    class Meta:
        model = Usuario
        fields = ["user", "perfil", "aniversario"]
        widgets = {
            "user": forms.HiddenInput(),
            "perfil": forms.Select(attrs={"class": "form-control"}),
            "aniversario": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.perfil != 1:
            self.fields.pop("perfil", None)


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        max_length=32,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=True,
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.CharField(
        required=True, widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        max_length=32,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=True,
    )
