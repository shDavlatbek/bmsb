from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from apps.utils.base_model import BaseModel
from apps.utils.mixins import SlugifyMixin
from tinymce.models import HTMLField


class MenuItem(MPTTModel):
    title = models.CharField(max_length=120)
    parent = TreeForeignKey(
        "self",
        null=True, blank=True,
        related_name="children",
        on_delete=models.CASCADE,
    )
    url = models.CharField(max_length=120)
    
    class MPTTMeta:
        order_insertion_by = ("title",)

    def get_absolute_url(self):
        return self.url

    def __str__(self):
        return self.title
    
    
class School(SlugifyMixin, BaseModel):
    domain = models.SlugField(unique=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = HTMLField()
    short_description = HTMLField()
    founded_year = models.SmallIntegerField()
    capacity = models.IntegerField()
    student_count = models.IntegerField()
    teacher_count = models.IntegerField()
    direction_count = models.IntegerField()
    class_count = models.IntegerField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=10, decimal_places=8)
    instagram_link = models.URLField()
    telegram_link = models.URLField()
    facebook_link = models.URLField()
    youtube_link = models.URLField()
    
    
    
    
