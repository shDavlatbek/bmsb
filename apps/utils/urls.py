from django.urls import path

from apps.utils.views import upload_image

urlpatterns = [
    path('tinymce-upload/', upload_image, name='tinymce_upload'),
]

