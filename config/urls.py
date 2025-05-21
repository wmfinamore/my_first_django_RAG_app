from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('rag/admin/', admin.site.urls),
    path('rag/api-auth/', include('rest_framework.urls')),
    path('rag/api/v1/', include('apps.api.urls')),
]


# Rota para ativar o debug toolbar quanto o django estiver em modo debug
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__', include(debug_toolbar.urls)),
    ] + urlpatterns