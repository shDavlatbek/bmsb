from django.urls import path

from .views import upload_image, APIDocumentationView

urlpatterns = [
    path('tinymce-upload/', upload_image, name='tinymce_upload'),
    path('docs/', APIDocumentationView.as_view(), name='api_documentation'),
]

