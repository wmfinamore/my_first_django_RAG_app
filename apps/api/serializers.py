from rest_framework import serializers
from apps.core.models import Index, IndexFile, IndexNode, IndexQuery


class IndexSerializer(serializers.ModelSerializer):
    files = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    queries = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Index
        fields = ['id', 'name', 'files', 'queries', 'created_at', 'updated_at', ]


class IndexFileSerializer(serializers.ModelSerializer):
    nodes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = IndexFile
        fields = ['id', 'index', 'file', 'nodes', 'original_filename', 'created_at', 'updated_at', ]


class IndexNodeSerializer(serializers.Serializer):

    class Meta:
        model = IndexNode
        fields = ['id', 'index_file', 'content', 'embedding', 'created_at', 'updated_at', ]


class IndexQuerySerializer(serializers.Serializer):

    class Meta:
        model = IndexQuery
        fields = ['id', 'index', 'messages', 'context_node_ids', 'created_at', 'updated_at', ]
