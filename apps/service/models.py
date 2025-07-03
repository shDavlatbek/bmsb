from django.db import models
from apps.common.mixins import SlugifyMixin
from apps.common.models import BaseModel
from apps.main.models import School
from apps.common.utils import generate_upload_path
from apps.common.validators import file_size
from tinymce.models import HTMLField



class Service(SlugifyMixin, BaseModel):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Maktab",
        related_name="services",
    )
    name = models.CharField(max_length=255, verbose_name="Nomi")
    slug = models.SlugField(max_length=255, verbose_name="Slug")
    description = HTMLField(verbose_name="Tavsifi")
    tags = models.CharField(max_length=255, verbose_name="Taglar", help_text="Taglarni probel bilan ajrating", null=True, blank=True)

    slug_source = 'name'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Xizmat"
        verbose_name_plural = "Xizmatlar"
        constraints = [
            models.UniqueConstraint(
                fields=['school', 'slug'],
                name='unique_service_school_slug',
            )
        ]


# Create your models here.
class CultureService(Service):
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    class Meta:
        verbose_name = "Madaniy xizmat"
        verbose_name_plural = "Madaniy xizmatlar"


class CultureServiceFile(BaseModel):
    service = models.ForeignKey(
        CultureService, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Xizmat",
        related_name="service_files",
    )
    file = models.FileField(
        upload_to=generate_upload_path,
        verbose_name="Fayl",
        validators=[file_size],
        help_text="Fayl 5 MB dan katta bo'lishi mumkin emas."
    )
    def __str__(self):
        return f"{self.service.name} - {self.created_at}"
    
    class Meta:
        verbose_name = "Xizmat fayli"
        verbose_name_plural = "Xizmat fayllari"


class Art(Service):
    email = models.EmailField(verbose_name="Email", null=True, blank=True)
    phone_number = models.CharField(max_length=255, verbose_name="Telefon raqami", null=True, blank=True)
    author_image = models.ImageField(
        upload_to=generate_upload_path,
        verbose_name="Muallif rasmi",
        validators=[file_size],
        help_text="Rasm 5 MB dan katta bo'lishi mumkin emas.",
        null=True, blank=True
    )
    author_name = models.CharField(max_length=255, verbose_name="Muallif ismi")
    author_musical_instrument = models.CharField(max_length=255, verbose_name="Muallif musiqaviy instrumenti", null=True, blank=True)
    author_direction = models.CharField(max_length=255, verbose_name="Muallif yo'nalishi", null=True, blank=True)
    author_honor = models.CharField(max_length=255, verbose_name="Muallif yutuqlari", null=True, blank=True)
    
    class Meta:
        abstract = True


class CultureArt(Art):
    class Meta:
        verbose_name = "Madaniy san'at"
        verbose_name_plural = "Madaniy san'at"


class FineArt(Art):
    class Meta:
        verbose_name = "Tasviriy san'at"
        verbose_name_plural = "Tasviriy san'at"


class ServiceImage(BaseModel):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Xizmat",
        related_name="service_images",
    )
    image = models.ImageField(
        upload_to=generate_upload_path,
        verbose_name="Rasm",
        validators=[file_size],
        help_text="Rasm 5 MB dan katta bo'lishi mumkin emas."
    )

    def __str__(self):
        return f"{self.service.name} - {self.created_at}"
    
    class Meta:
        verbose_name = "Xizmat rasmi"
        verbose_name_plural = "Xizmat rasmlari"