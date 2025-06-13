from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.common.mixins import DescriptionMixin, SchoolAdminMixin, AdminTranslation
from mptt.admin import DraggableMPTTAdmin
from modeltranslation.admin import TranslationTabularInline
from modeltranslation import settings as mt_settings
from django.utils.translation import gettext_lazy as _
from . import models
from django.utils.safestring import mark_safe


@admin.register(models.Menu)
class MenuAdmin(SchoolAdminMixin, AdminTranslation, DraggableMPTTAdmin):
    class Media:
        css = {
            'screen': ('css/admin_menu.css',),
        }


@admin.register(models.School)
class SchoolAdmin(DescriptionMixin, SchoolAdminMixin, AdminTranslation):
    list_display = ('name', 'domain', 'is_active')
    search_fields = ('name', 'domain')
    list_filter = ('is_active',)
    fieldsets = (
        ('Asosiy 📌',
            {'fields': ('is_active', 'domain', 'name', 'slug', 'description', 'short_description')}
        ),
        ('Raqamlar 📊', {'fields': ('founded_year', 'capacity', 'student_count', 'teacher_count', 'direction_count', 'class_count')}),
        ('Kontaktlar 📞', {'fields': ('email', 'phone_number', 'address', 'latitude', 'longitude')}),
        ('Ijtimoiy tarmoqlar 🔗', {'fields': ('instagram_link', 'telegram_link', 'facebook_link', 'youtube_link')}),
    )
    prepopulated_fields = {
        'slug': ('name',),
    }
    
    def get_readonly_fields(self, request, obj=None):
        ro = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            ro += ['domain', 'is_active']
        return ro

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        return obj.pk == request.user.school_id
    

@admin.register(models.Banner)
class BannerAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ('image_tag', 'title', 'is_active')
    search_fields = ('title',)
    list_filter = ('is_active',)
    list_display_links = ('image_tag', 'title')


@admin.register(models.SchoolLife)
class SchoolLifeAdmin(DescriptionMixin, SchoolAdminMixin, AdminTranslation):
    list_display = ('image_tag', 'title', 'is_active')
    search_fields = ('title',)
    list_filter = ('is_active',)
    list_display_links = ('image_tag', 'title')
    

@admin.register(models.Direction)
class DirectionAdmin(DescriptionMixin, AdminTranslation):
    list_display = ('name', 'icon_preview', 'image_preview', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)
    list_display_links = ('name',)
    prepopulated_fields = {
        'slug': ('name',),
    }
    readonly_fields = ('icon_display', 'image_display')
    
    def icon_preview(self, obj):
        """Display icon thumbnail in list view"""
        if obj.icon:
            return mark_safe(f'<img src="{obj.icon.url}" style="height: 30px; width: 30px; object-fit: cover; border-radius: 4px;" />')
        return ""
    icon_preview.short_description = "Ikonka"
    
    def image_preview(self, obj):
        """Display image thumbnail in list view"""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="height: 30px; width: 50px; object-fit: cover; border-radius: 4px;" />')
        return ""
    image_preview.short_description = "Fon rasmi"
    
    def icon_display(self, obj):
        """Display icon in detail view"""
        if obj.icon:
            return mark_safe(f'<img src="{obj.icon.url}" style="height: 100px; object-fit: cover; border-radius: 8px;" />')
        return ""
    icon_display.short_description = "Ikonka ko'rinishi"
    
    def image_display(self, obj):
        """Display background image in detail view"""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="height: 150px; object-fit: cover; border-radius: 8px;" />')
        return ""
    image_display.short_description = "Fon rasmi ko'rinishi"


@admin.register(models.Subject)
class SubjectAdmin(DescriptionMixin, AdminTranslation):
    list_display = ('name', 'image_preview', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)
    list_display_links = ('name',)
    prepopulated_fields = {
        'slug': ('name',),
    }
    readonly_fields = ('image_display',)
    
    def image_preview(self, obj):
        """Display image thumbnail in list view"""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="height: 30px; width: 50px; object-fit: cover; border-radius: 4px;" />')
        return ""
    image_preview.short_description = "Fon rasmi"
    
    def image_display(self, obj):
        """Display background image in detail view"""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="height: 150px; object-fit: cover; border-radius: 8px;" />')
        return ""
    image_display.short_description = "Fon rasmi ko'rinishi"


@admin.register(models.MusicalInstrument)
class MusicalInstrumentAdmin(DescriptionMixin, AdminTranslation):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)
    list_display_links = ('name',)
    prepopulated_fields = {
        'slug': ('name',),
    }


class TeacherExperienceInline(TranslationTabularInline):
    model = models.TeacherExperience
    extra = 0
    class Media:
        js = (
            "admin/js/jquery.init.js",
            "modeltranslation/js/force_jquery.js",
            mt_settings.JQUERY_UI_URL,
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "all": ("modeltranslation/css/tabbed_translation_fields.css", "css/admin_translation.css",),
        }

@admin.register(models.Teacher)
class TeacherAdmin(DescriptionMixin, SchoolAdminMixin, admin.ModelAdmin):
    list_display = ('full_name', 'is_active')
    search_fields = ('full_name',)
    list_filter = ('is_active',)
    list_display_links = ('full_name',)
    inlines = [TeacherExperienceInline]
    prepopulated_fields = {
        'slug': ('full_name',),
    }

@admin.register(models.DirectionSchool)
class DirectionSchoolAdmin(DescriptionMixin, SchoolAdminMixin, admin.ModelAdmin):
    def has_add_permission(self, request):
        # Allow adding only if there's no existing DirectionSchool for the current school
        if request.user.is_superuser:
            return False
        
        # For non-superusers, check if DirectionSchool already exists for their school
        if hasattr(request.user, 'school_id') and request.user.school_id:
            existing_instance = models.DirectionSchool.objects.filter(school_id=request.user.school_id).exists()
            return not existing_instance
        
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Allow superusers to delete, but prevent regular users from deleting
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return False
    

@admin.register(models.FAQ)
class FAQAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ('title', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('title', 'description',)
    
    # fieldsets = (
    #     ('Asosiy ma\'lumotlar 📌', {
    #         'fields': ('school', 'title', 'is_active')
    #     }),
    #     ('Javob 💬', {
    #         'fields': ('description',)
    #     }),
    # )


@admin.register(models.Vacancy)
class VacancyAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ('title', 'type', 'salary', 'location', 'is_active', 'created_at')
    list_filter = ('is_active', 'type', 'created_at')
    search_fields = ('title', 'description', 'requirements', 'location')
    prepopulated_fields = {'slug': ('title',)}
    
    def get_form(self, request, obj=None, **kwargs):
        """Override form to show choice labels in admin"""
        form = super().get_form(request, obj, **kwargs)
        return form


@admin.register(models.Document)
class DocumentAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ('title', 'category', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('title',)


@admin.register(models.TimeTable)
class TimeTableAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ('title', 'file', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)
    
    def has_add_permission(self, request):
        # Prevent adding new timetables (they should be created automatically)
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deleting timetables
        return False


@admin.register(models.DocumentCategory)
class DocumentCategoryAdmin(AdminTranslation):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)


@admin.register(models.Staff)
class StaffAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ('full_name', 'position', 'experience_years', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('full_name', 'position')
    prepopulated_fields = {'slug': ('full_name',)}


@admin.register(models.Leader)
class LeaderAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ('full_name', 'position', 'working_days', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('full_name', 'position', 'description')
    prepopulated_fields = {'slug': ('full_name',)}