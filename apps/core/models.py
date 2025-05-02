from django.db import models


class TimeStampedModel(models.Model):
    """
    Uma classe abstrata que provê auto atualização ao criar e alterar registros de uma tabela.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
