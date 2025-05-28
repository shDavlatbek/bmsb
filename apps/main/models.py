from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True, verbose_name="Kenglik")
    longitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True, verbose_name="Uzunlik")
    instagram_link = models.URLField(null=True, blank=True, verbose_name="Instagram havola")
    telegram_link = models.URLField(null=True, blank=True, verbose_name="Telegram havola")
    facebook_link = models.URLField(null=True, blank=True, verbose_name="Facebook havola")
    youtube_link = models.URLField(null=True, blank=True, verbose_name="Youtube havola")
    
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
    description = models.TextField(null=True, blank=True, verbose_name="Tafsilot")
    
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
        verbose_name="Maktab",
        related_name="menus",
    )
    
    title = models.CharField(max_length=120)
    parent = TreeForeignKey(
        "self",
        null=True, blank=True,
        related_name="children",
        on_delete=models.CASCADE,
    )
    url = models.CharField(max_length=255, null=True, blank=True)
    
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
        

class DirectionSchool(BaseModel):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE,
        verbose_name="Maktab",
        related_name="directions",
        null=True, blank=True,
    )
    directions = models.ManyToManyField(
        'Direction',
        verbose_name="Yo'nalishlar",
        related_name="direction_schools",
        blank=True
    )
    
    def __str__(self):
        return "Yo'nalishlar"
    
    class Meta:
        verbose_name = "Maktab yo'nalishlari "
        verbose_name_plural = "Maktab yo'nalishlari"
        # constraints = [
        #     models.UniqueConstraint(fields=['school'], name='unique_direction_school_per_school')
        # ]


class Subject(SlugifyMixin, BaseModel):
    name = models.CharField(max_length=255, verbose_name="Nomi")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    
    description = models.TextField(null=True, blank=True, verbose_name="Tafsilot")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Fan "
        verbose_name_plural = "Fanlar"
    


class MusicalInstrument(SlugifyMixin, BaseModel):
    name = models.CharField(max_length=255, verbose_name="Nomi")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    
    description = models.TextField(null=True, blank=True, verbose_name="Tafsilot")
    
    class Meta:
        verbose_name = "Musiqa asbobi "
        verbose_name_plural = "Musiqa asboblari"
    


class Direction(SlugifyMixin, BaseModel):
    name = models.CharField(max_length=255, verbose_name="Nomi")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    
    description = HTMLField(null=True, blank=True, verbose_name="Tafsilot")
    
    founded_year = models.SmallIntegerField(null=True, blank=True, verbose_name="Ishga tushgan yili")
    student_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="O'quvchilar soni")
    teacher_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="O'qituvchilar soni")
    
    subjects = models.ManyToManyField(
        Subject,
        verbose_name="Fanlar",
        related_name="directions",
        blank=True
    )
    musical_instruments = models.ManyToManyField(
        MusicalInstrument,
        verbose_name="Musiqa asboblari",
        related_name="directions",
        blank=True
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Yo'nalish "
        verbose_name_plural = "Yo'nalishlar"


class Teacher(BaseModel):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Maktab",
        related_name="teachers",
    )
    full_name = models.CharField(max_length=500, verbose_name="F.I.O")
    image = models.ImageField(upload_to=generate_upload_path, verbose_name="Rasm", validators=[file_size], 
                              help_text="Rasm 5 MB dan katta bo'lishi mumkin emas.")
    
    directions = models.ManyToManyField(
        Direction,
        verbose_name="Yo'nalishlar",
        related_name="teachers",
        blank=True,
    )
    experience_years = models.PositiveIntegerField(null=True, blank=True, verbose_name="Tajribasi", help_text="Yil")
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = "O'qituvchi "
        verbose_name_plural = "O'qituvchilar"
    

class TeacherExperience(BaseModel):
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE,
        verbose_name="O'qituvchi",
        related_name="experiences",
    )
    
    title = models.CharField(max_length=255, verbose_name="Lavozimi")
    start_date = models.DateField(verbose_name="Boshlanish sanasi", null=True, blank=True)
    end_date = models.DateField(verbose_name="Tugash sanasi", null=True, blank=True)
    
    def __str__(self):
        return f"{self.teacher.full_name} - {self.title}"
    
    class Meta:
        verbose_name = "O'qituvchi tajribasi "
        verbose_name_plural = "O'qituvchi tajribalari"



# Signal to create default instances when a new School is created
@receiver(post_save, sender=School)
def create_school_defaults(sender, instance, created, **kwargs):
    """
    Create default instances and set default values when a new School is created.
    """
    if created:
        # Set default values for the school if not provided
        if not instance.capacity:
            instance.capacity = 0
        if not instance.student_count:
            instance.student_count = 0
        if not instance.teacher_count:
            instance.teacher_count = 0
        if not instance.direction_count:
            instance.direction_count = 0
        if not instance.class_count:
            instance.class_count = 0
        
        # Save the instance with default values
        instance.save()
        
        # Create hierarchical menu structure
        # Main menu items with their children
        menu_structure = {
            "Maktab": {
                "url": "#",
                "children": [
                    {"title": "Maktab haqida", "url": "#"},
                    {"title": "Rahbariyat va o'qituvchilar xodimlar", "url": "#"},
                    {"title": "Bo'sh ish o'rinlari", "url": "#"},
                ]
            },
            "Faoliyat": {
                "url": "#",
                "children": [
                    {"title": "Yo'nalishlar", "url": "#"},
                    {"title": "Tadbirlar", "url": "#"},
                    {"title": "Tanlov va festivallar", "url": "#"},
                    {"title": "Maktabimiz faxrlariz", "url": "#"},
                    {"title": "Mahorat darslari", "url": "#"},
                ]
            },
            "Ta'lim jarayoni": {
                "url": "#",
                "children": [
                    {"title": "O'quv reja va dastur", "url": "#"},
                    {"title": "Ta'limga oid ma'lumotlar", "url": "#"},
                    {"title": "Resurslar (🔗 YouTube, PDF darsliklar)", "url": "#"},
                ]
            },
            "Matbuot": {
                "url": "#",
                "children": [
                    {"title": "Yangiliklar va e'lonlar", "url": "#"},
                    {"title": "Media (rasm va videolar)", "url": "#"},
                ]
            },
            "Hujjatlar": {
                "url": "#",
                "children": [
                    {"title": "Rasmiy hujjatlar", "url": "#"},
                    {"title": "Ochiq ma'lumotlar", "url": "#"},
                ]
            },
            "Tijoriy bo'lim": {
                "url": "#",
                "children": [
                    {"title": "Madaniy xizmatlar", "url": "#"},
                    {"title": "Amaliy san'at", "url": "#"},
                    {"title": "Tasviriy san'at", "url": "#"},
                ]
            },
            "Bog'lanish": {
                "url": "#",
                "children": []
            }
        }
        
        # Create menu items
        for parent_title, parent_data in menu_structure.items():
            # Create parent menu item
            parent_menu = Menu.objects.create(
                school=instance,
                title=parent_title,
                url=parent_data["url"],
                parent=None
            )
            
            # Create child menu items
            for child_data in parent_data["children"]:
                Menu.objects.create(
                    school=instance,
                    title=child_data["title"],
                    url=child_data["url"],
                    parent=parent_menu
                )
        
        # Create a DirectionSchool instance for the new school
        DirectionSchool.objects.create(school=instance)
        
        # You can add more default instances here as needed
        # For example, create default subjects or musical instruments
        
        print(f"Default instances created for school: {instance.name}")
