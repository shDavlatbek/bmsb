from django.db import models
from django.core.exceptions import ValidationError
import re
import requests
from urllib.parse import urlparse, parse_qs

from apps.common.mixins import SlugifyMixin
from apps.common.models import BaseModel
from apps.common.utils import generate_upload_path
from apps.common.validators import file_size_50, validate_youtube_link


class ResourceVideo(BaseModel):
    school = models.ForeignKey(
        'main.School', on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Maktab",
        related_name="resource_videos",
    )
    
    title = models.CharField(max_length=255, verbose_name="Nomi")
    youtube_link = models.URLField(verbose_name="Youtube havola", validators=[validate_youtube_link])
    view_count = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Resurs video "
        verbose_name_plural = "Resurs videolar"



class ResourceFile(BaseModel):
    school = models.ForeignKey(
        'main.School', on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Maktab",
        related_name="resource_files",
    )
    
    title = models.CharField(max_length=255, verbose_name="Nomi")
    file = models.FileField(
        upload_to=generate_upload_path, 
        verbose_name="Fayl", 
        validators=[file_size_50],
        help_text="Fayl 50 MB dan katta bo'lishi mumkin emas."
    )
    download_count = models.PositiveIntegerField(default=0, verbose_name="Yuklab olishlar soni")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Resurs fayl "
        verbose_name_plural = "Resurs fayllar"
