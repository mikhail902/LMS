from rest_framework.documentation import include_docs_urls
from django.urls import path
from django.urls import include


urlpatterns = [
    path('docs/', include_docs_urls(title='API Documentation')),
    path('', include('docs.urls')),
]