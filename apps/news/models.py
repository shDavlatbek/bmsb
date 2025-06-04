from django.contrib import admin
from django.db import models
from apps.common.models import BaseModel
from apps.common.mixins import SlugifyMixin
from apps.common.utils import generate_upload_path
from apps.common.validators import file_size
from tinymce.models import HTMLField
from django.utils.safestring import mark_safe


class Category(SlugifyMixin, BaseModel):
    school = models.ForeignKey(
        'main.School', on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Maktab",
        related_name="news_categories",
    )
    
    name = models.CharField(max_length=255, verbose_name="Nomi")
    slug = models.SlugField(verbose_name="Slug")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['school', 'slug'],
                name='unique_newscategory_school_slug',
            )
        ]


class News(SlugifyMixin, BaseModel):
    school = models.ForeignKey(
        'main.School', on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Maktab",
        related_name="news",
    )
    
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        verbose_name="Kategoriya",
        related_name="news",
    )
    
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    slug = models.SlugField(verbose_name="Slug")
    image = models.ImageField(
        upload_to=generate_upload_path, 
        verbose_name="Rasm", 
        validators=[file_size], 
        help_text="Rasm 5 MB dan katta bo'lishi mumkin emas."
    )
    content = HTMLField(verbose_name="Tafsilot")
    view_count = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")
    
    @admin.display(description="Rasm")
    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" style="height: 50px; object-fit: cover;" />')
        return "Rasm yo'q"
    
    def increment_view_count(self):
        """Method to increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['school', 'slug'],
                name='unique_news_school_slug',
            )
        ]
