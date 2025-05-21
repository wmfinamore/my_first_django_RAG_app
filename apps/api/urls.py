from django.urls import path
from rest_framework.authtoken import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (IndexList, IndexDetail, IndexNodeList, IndexNodeDetail, IndexFileDetail, IndexQueryDetail,
                    IndexQueryList)
from .auth import LoginView, RegisterView


urlpatterns = [
    path('indexes/', IndexList.as_view(), name='index-list'),
    path('indexes/<int:pk>/', IndexDetail.as_view(), name='index-detail'),
    path('index-files/', IndexFileDetail.as_view(), name='indexfile-list'),
    path('index-files/<int:pk>/', IndexFileDetail.as_view(), name='indexfile-detail'),
    path('index-nodes/', IndexNodeList.as_view(), name='indexnode-list'),
    path('index-nodes/<int:pk>/', IndexNodeDetail.as_view(), name='indexnode-detail'),
    path('index-queries/', IndexQueryList.as_view(), name='indexquery-list'),
    path('index-queries/<int:pk>/', IndexQueryDetail.as_view(), name='indexquery-detail'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/register/', RegisterView.as_view(), name='register'),

]

urlpatterns = format_suffix_patterns(urlpatterns) # permite que os clientes possam especificar o formato de retorno

urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token),
]
