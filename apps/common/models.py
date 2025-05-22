from apps.common.utils import compress
import os
import uuid
from django.db import models
from django.db.models import QuerySet


class ActiveQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True)
        
    def inactive(self):
        return self.filter(is_active=False)


class ActiveManager(models.Manager):
    def get_queryset(self):
        return ActiveQuerySet(self.model, using=self._db)
        
    def active(self):
        return self.get_queryset().active()
        
    def inactive(self):
        return self.get_queryset().inactive()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan sana")
    is_active = models.BooleanField(default=True, verbose_name="Faoligi")
    
    objects = ActiveManager()
    
    class Meta:
        abstract = True


################################################
#--------------- TINYMCE IMAGE ----------------#
################################################

def get_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('uploads', 'tinymce', filename)


class TinyMCEImage(models.Model):
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to=get_image_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title or f"Image {self.id}"
    
    def save(self, *args, **kwargs):
        if not self.title and self.image:
            self.title = os.path.basename(self.image.name)
            
        if self.image:
            self.image = compress(self.image)
        
        super().save(*args, **kwargs)