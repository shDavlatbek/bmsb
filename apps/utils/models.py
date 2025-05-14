import os
import uuid
from django.db import models


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
        super().save(*args, **kwargs)