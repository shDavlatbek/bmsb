from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from apps.common.mixins import SlugifyMixin
from tinymce.models import HTMLField
from django.utils.safestring import mark_safe

from apps.common.models import BaseModel
from apps.common.utils import generate_upload_path
from apps.common.validators import file_size

    
    
class School(SlugifyMixin, BaseModel):
    domain = models.SlugField(unique=True, verbose_name="Subdomen")
    name = models.CharField(max_length=255, verbose_name="Nomi")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = HTMLField(null=True, blank=True, verbose_name="Tafsilot")
    short_description = HTMLField(null=True, blank=True, verbose_name="Qisqacha tafsilot")
    founded_year = models.SmallIntegerField(null=True, blank=True, verbose_name="Ishga tushgan yili")
    capacity = models.PositiveIntegerField(null=True, blank=True, verbose_name="O'quvchilar sig'imi")
    student_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="O'quvchilar soni")
    teacher_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="O'qituvchilar soni")
    direction_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="Yo'nalishlar soni")
    class_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="Sinflar soni")
    email = models.EmailField(null=True, blank=True, verbose_name="Email")
    phone_number = models.CharField(max_length=255, null=True, blank=True, verbose_name="Telefon raqami")
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Manzil")
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True, verbose_name="Latitude")
    longitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True, verbose_name="Longitude")
    instagram_link = models.URLField(null=True, blank=True, verbose_name="Instagram link")
    telegram_link = models.URLField(null=True, blank=True, verbose_name="Telegram link")
    facebook_link = models.URLField(null=True, blank=True, verbose_name="Facebook link")
    youtube_link = models.URLField(null=True, blank=True, verbose_name="Youtube link")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Maktab "
        verbose_name_plural = "Maktablar"


class SchoolLife(BaseModel):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Maktab",
        related_name="school_lives",
    )
    
    image = models.ImageField(upload_to=generate_upload_path, verbose_name="Rasm", validators=[file_size], 
                              help_text="Rasm 5 MB dan katta bo'lishi mumkin emas.")
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    description = HTMLField(null=True, blank=True, verbose_name="Tafsilot")
    
    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" style="height: 50px; object-fit: cover;" />')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Maktab hayoti "
        verbose_name_plural = "Maktab hayoti"


class Menu(MPTTModel):
    school = models.ForeignKey(
        'School', on_delete=models.CASCADE,
        null=True, blank=True,
    )
    
    title = models.CharField(max_length=120)
    parent = TreeForeignKey(
        "self",
        null=True, blank=True,
        related_name="children",
        on_delete=models.CASCADE,
    )
    url = models.CharField(max_length=255)
    
    class MPTTMeta:
        order_insertion_by = ("title",)

    def get_absolute_url(self):
        return self.url

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Menu "
        verbose_name_plural = "Menu"


class Banner(BaseModel):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Maktab",
        related_name="banners",
    )
    
    image = models.ImageField(upload_to=generate_upload_path, verbose_name="Rasm", validators=[file_size], 
                              help_text="Rasm 5 MB dan katta bo'lishi mumkin emas.")
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    button_text = models.CharField(max_length=255, null=True, blank=True, verbose_name="Tugma matni")
    link = models.URLField(null=True, blank=True, verbose_name="Havola")
    
    
    def __str__(self):
        return self.title
    
    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" style="height: 50px; object-fit: cover;" />')
    
    class Meta:
        verbose_name = "Banner "
        verbose_name_plural = "Bannerlar"
