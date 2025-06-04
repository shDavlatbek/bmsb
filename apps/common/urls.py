from django.urls import path

from .views import upload_image

urlpatterns = [
    path('tinymce-upload/', upload_image, name='tinymce_upload'),
]

