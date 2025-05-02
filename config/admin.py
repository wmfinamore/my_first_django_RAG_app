from django.contrib.admin import AdminSite


class RAGAdminSite(AdminSite):
    # classe o django admin customizado
    site_header = 'RAG Administration'
    site_title = 'RAG Administration'
    index_title = 'Welcome to RAG Administration'
    site_url = '/rag'
