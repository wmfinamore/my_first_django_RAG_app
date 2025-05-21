from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from  apps.core.models import Index, IndexFile, IndexNode, IndexQuery
from .serializers import IndexSerializer, IndexFileSerializer, IndexNodeSerializer, IndexQuerySerializer
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django.contrib.postgres.search import SearchVector, SearchQuery
from rest_framework.filters import SearchFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAdminUser
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly


class IndexFilter(FilterSet):

    class Meta:
        model = Index
        fields = ['name', ]


class CustomPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class IndexList(ListCreateAPIView):
    queryset = Index.objects.all()
    serializer_class = IndexSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = IndexFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]


class IndexDetail(RetrieveUpdateDestroyAPIView):
    queryset = Index.objects.all()
    serializer_class = IndexSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class IndexFileList(ListCreateAPIView):
    queryset = IndexFile.objects.all()
    serializer_class = IndexFileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class IndexFileDetail(RetrieveUpdateDestroyAPIView):
    queryset = IndexFile.objects.all()
    serializer_class = IndexFileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class IndexNodeList(ListCreateAPIView):
    queryset = IndexNode.objects.all()
    serializer_class = IndexNodeSerializer
    filter_backends = [SearchFilter]
    search_fields = ['content']

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        search_query = self.request.query_params.get('search')
        if search_query:
            query = SearchQuery(search_query)
            vector = SearchVector('content')
            queryset = queryset.annotate(search=vector).filter(search=query)
        return queryset


class IndexNodeDetail(RetrieveUpdateDestroyAPIView):
    queryset = IndexNode.objects.all()
    serializer_class = IndexNodeSerializer


class IndexQueryList(ListCreateAPIView):
    queryset = IndexQuery.objects.all()
    serializer_class = IndexQuerySerializer


class IndexQueryDetail(RetrieveUpdateDestroyAPIView):
    queryset = IndexQuery.objects.all()
    serializer_class = IndexQuerySerializer
