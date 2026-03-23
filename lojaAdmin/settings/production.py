from .base import *

DEBUG = False

SECRET_KEY = "troque-essa-chave-em-producao"

ALLOWED_HOSTS = ["seu-dominio.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
