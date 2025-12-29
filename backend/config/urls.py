"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import (
    workspace, create_document, get_document, update_document, 
    delete_document, reorder_documents, sync_ai_twin, ai_assist
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', workspace, name='workspace'),  # This makes it the home page
    path('create-doc/', create_document, name='create_document'),
    path('doc/<int:doc_id>/', get_document, name='get_document'),
    path('doc/<int:doc_id>/update/', update_document, name='update_document'),
    path('doc/<int:doc_id>/delete/', delete_document, name='delete_document'),
    path('doc/<int:doc_id>/sync/', sync_ai_twin, name='sync_ai_twin'),  # AI Twin sync
    path('reorder-docs/', reorder_documents, name='reorder_documents'),
    path('ai-assist/', ai_assist, name='ai_assist'),  # AI text assistant
]
