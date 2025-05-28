from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.common.mixins import DescriptionMixin, SchoolAdminMixin, AdminTranslation
from mptt.admin import DraggableMPTTAdmin
from modeltranslation.admin import TranslationTabularInline
from modeltranslation import settings as mt_settings
from django.utils.translation import gettext_lazy as _
from . import models


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
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)
    list_display_links = ('name',)
    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(models.Subject)
class SubjectAdmin(DescriptionMixin, AdminTranslation):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)
    list_display_links = ('name',)
    prepopulated_fields = {
        'slug': ('name',),
    }


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
        return False