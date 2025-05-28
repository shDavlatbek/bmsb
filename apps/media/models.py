from django.db import models
from django.core.exceptions import ValidationError
import re
import requests
from urllib.parse import urlparse, parse_qs

from apps.common.models import BaseModel
from apps.common.utils import generate_upload_path
from apps.common.validators import file_size, validate_youtube_link



class MediaCollection(BaseModel):
    school = models.ForeignKey(
        'main.School', on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Maktab",
        related_name="media_collections",
    )
    
    title = models.CharField(max_length=255, verbose_name="Nomi")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Rasmlar to'plami "
        verbose_name_plural = "Rasmlar to'plami"


class MediaImage(BaseModel):
    show_in_main = models.BooleanField(default=False, verbose_name="Asosiy sahifada ko'rsatish")
    image = models.ImageField(upload_to=generate_upload_path, verbose_name="Rasm", validators=[file_size], 
                              help_text="Rasm 5 MB dan katta bo'lishi mumkin emas.")
    
    collection = models.ForeignKey(
        MediaCollection, on_delete=models.CASCADE,
        verbose_name="Rasmlar to'plami",
        related_name="media_images",
    )
    
    def __str__(self):
        return f"{self.collection.title} - {self.image.name}"
    
    class Meta:
        verbose_name = "Rasm "
        verbose_name_plural = "Rasmlar"


class MediaVideo(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Nomi")
    youtube_link = models.URLField(verbose_name="Youtube havola", validators=[validate_youtube_link])
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Video "
        verbose_name_plural = "Videolar"