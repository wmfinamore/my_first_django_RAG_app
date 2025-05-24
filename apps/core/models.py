from django.db import models
from django.contrib.auth import get_user_model
from pgvector.django import VectorField
from pgvector.django import HnswIndex


class TimeStampedModel(models.Model):
    """
    Uma classe abstrata que provê auto atualização ao criar e alterar registros de uma tabela.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


CustomUser = get_user_model()


class Index(TimeStampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, help_text='Which user owns the index')
    name = models.CharField(max_length=128)

    class Meta:
        ordering = ['name',]


def get_index_file_location(instance, filename):
    return f'indexes/{instance.index.id}/{filename}'


class IndexFile(TimeStampedModel):
    index = models.ForeignKey(Index, related_name='files', on_delete=models.PROTECT,
                              help_text='Which index the file belongs to')
    file = models.FileField(upload_to=get_index_file_location, help_text='The file uploaded for the index')
    original_filename = models.CharField(max_length=255, help_text='The original filename uploaded by the user')


class IndexNode(TimeStampedModel):
    index_file = models.ForeignKey(IndexFile, related_name='nodes', on_delete=models.PROTECT,
                                   help_text='The index file node is associated with')
    content = models.TextField(help_text='Content of the node, consisting of few sentences from the document.')
    embedding = VectorField(dimensions=384, help_text='384 sized embedding for MniLM L6 V2.')

    class Meta:
        indexes = [
            HnswIndex(fields=['embedding'], opclasses=["vector_cosine_ops"], name='indexnode_embedding_index'),
        ]


class IndexQuery(TimeStampedModel):
    index = models.ForeignKey(Index, related_name='queries', on_delete=models.PROTECT,
                              help_text='Reference to the Index related to this query.')
    messages = models.JSONField(help_text='List of messages exchanged with the assistant.')
    context_node_ids = models.JSONField(help_text='List of IndexNode IDs used as context for the query.')


STATUS_CHOICE = [
    ['PENDING', 'PENDING'],
    ['SUCCESS', 'SUCCESS'],
    ['FAILURE', 'FAILURE'],
    ['REVOKED', 'REVOKED']
]


class TaskStatus(TimeStampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, help_text='User who initiated the task')
    task_id = models.CharField(max_length=255, help_text='Celery task ID')
    task_name = models.CharField(max_length=255, help_text='Name of the task')
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default='PENDING')
    result = models.TextField(blank=True, null=True, help_text='Text result or error message')
