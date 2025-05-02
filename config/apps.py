from django.contrib.admin.apps import AdminConfig


class RAGAdminConfig(AdminConfig):
    #registro da customização do django admin
    default_site = 'config.admin.RAGAdminSite'
    verbose_name = 'RAG Administration'
    verbose_name_plural = 'RAG Administration'
