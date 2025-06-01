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
        order_insertion_by = ("id",)

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
    image = models.ImageField(
        upload_to=generate_upload_path, 
        verbose_name="Fon rasmi", 
        validators=[file_size],
        null=True, blank=True,
        help_text="Rasm 5 MB dan katta bo'lishi mumkin emas."
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Fan "
        verbose_name_plural = "Fanlar"
    


class MusicalInstrument(SlugifyMixin, BaseModel):
    name = models.CharField(max_length=255, verbose_name="Nomi")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    
    description = models.TextField(null=True, blank=True, verbose_name="Tafsilot")
    image = models.ImageField(
        upload_to=generate_upload_path, 
        verbose_name="Fon rasmi", 
        validators=[file_size],
        null=True, blank=True,
        help_text="Rasm 5 MB dan katta bo'lishi mumkin emas."
    )
    
    class Meta:
        verbose_name = "Musiqa asbobi "
        verbose_name_plural = "Musiqa asboblari"
    


class Direction(SlugifyMixin, BaseModel):
    name = models.CharField(max_length=255, verbose_name="Nomi")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    slug_source = "name"
    description = HTMLField(null=True, blank=True, verbose_name="Tafsilot")
    
    icon = models.ImageField(
        upload_to=generate_upload_path, 
        verbose_name="Ikonka", 
        validators=[file_size],
        null=True, blank=True,
        help_text="Rasm 5 MB dan katta bo'lishi mumkin emas."
    )
    image = models.ImageField(
        upload_to=generate_upload_path, 
        verbose_name="Fon rasmi", 
        validators=[file_size],
        null=True, blank=True,
        help_text="Rasm 5 MB dan katta bo'lishi mumkin emas."
    )
    
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


class Teacher(SlugifyMixin, BaseModel):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Maktab",
        related_name="teachers",
    )
    full_name = models.CharField(max_length=500, verbose_name="F.I.O")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    slug_source = "full_name"
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


class FAQ(BaseModel):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Maktab",
        related_name="faqs",
    )
    
    title = models.CharField(max_length=255, verbose_name="Savol")
    description = models.TextField(verbose_name="Javob")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "FAQ "
        verbose_name_plural = "FAQ"


class Vacancy(SlugifyMixin, BaseModel):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Maktab",
        related_name="vacancies",
    )
    
    title = models.CharField(max_length=255, verbose_name="Lavozim nomi")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Tafsilot")
    salary = models.CharField(max_length=255, verbose_name="Maosh", null=True, blank=True)
    requirements = models.TextField(verbose_name="Talablar")
    location = models.CharField(max_length=255, verbose_name="Joylashuv", null=True, blank=True)
    
    VACANCY_TYPES = [
        ('full_time', "To'la ish kuni"),
        ('part_time', "Yarim ish kuni"),
        ('contract', "Shartnoma asosida"),
        ('internship', "Amaliyot"),
        ('remote', "Masofaviy ish"),
    ]
    
    type = models.CharField(
        max_length=50,
        choices=VACANCY_TYPES,
        default='full_time',
        verbose_name="Ish turi"
    )
    
    # SlugifyMixin configuration
    slug_field = 'slug'
    slug_source = 'title'
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Vakansiya "
        verbose_name_plural = "Vakansiyalar"
        unique_together = [['school', 'slug']]


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
        
        # Create hierarchical menu structure in correct order
        # Using ordered list instead of dictionary to maintain order
        menu_structure = [
            {
                "title": "Maktab",
                "url": "#",
                "children": [
                    {"title": "Maktab haqida", "url": "#"},
                    {"title": "Rahbariyat va o'qituvchilar xodimlar", "url": "#"},
                    {"title": "Bo'sh ish o'rinlari", "url": "#"},
                ]
            },
            {
                "title": "Faoliyat",
                "url": "#",
                "children": [
                    {"title": "Yo'nalishlar", "url": "#"},
                    {"title": "Tadbirlar", "url": "#"},
                    {"title": "Tanlov va festivallar", "url": "#"},
                    {"title": "Maktabimiz faxrlariz", "url": "#"},
                    {"title": "Mahorat darslari", "url": "#"},
                ]
            },
            {
                "title": "Ta'lim jarayoni",
                "url": "#",
                "children": [
                    {"title": "O'quv reja va dastur", "url": "#"},
                    {"title": "Ta'limga oid ma'lumotlar", "url": "#"},
                    {"title": "Resurslar (🔗 YouTube, PDF darsliklar)", "url": "#"},
                ]
            },
            {
                "title": "Matbuot",
                "url": "#",
                "children": [
                    {"title": "Yangiliklar va e'lonlar", "url": "#"},
                    {"title": "Media (rasm va videolar)", "url": "#"},
                ]
            },
            {
                "title": "Hujjatlar",
                "url": "#",
                "children": [
                    {"title": "Rasmiy hujjatlar", "url": "#"},
                    {"title": "Ochiq ma'lumotlar", "url": "#"},
                ]
            },
            {
                "title": "Tijoriy bo'lim",
                "url": "#",
                "children": [
                    {"title": "Madaniy xizmatlar", "url": "#"},
                    {"title": "Amaliy san'at", "url": "#"},
                    {"title": "Tasviriy san'at", "url": "#"},
                ]
            },
            {
                "title": "Bog'lanish",
                "url": "#",
                "children": []
            }
        ]
        
        # Create menu items in correct order
        for menu_data in menu_structure:
            # Create parent menu item
            parent_menu = Menu.objects.create(
                school=instance,
                title=menu_data["title"],
                url=menu_data["url"],
                parent=None
            )
            
            # Create child menu items
            for child_data in menu_data["children"]:
                Menu.objects.create(
                    school=instance,
                    title=child_data["title"],
                    url=child_data["url"],
                    parent=parent_menu
                )
        
        # Create a DirectionSchool instance for the new school
        DirectionSchool.objects.create(school=instance)