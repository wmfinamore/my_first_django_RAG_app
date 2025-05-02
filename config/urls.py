from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('rag/admin/', admin.site.urls),
]


# Rota para ativar o debug toolbar quanto o django estiver em modo debug
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__', include(debug_toolbar.urls)),
    ] + urlpatterns