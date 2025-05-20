from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.common.mixins import DescriptionMixin, SchoolAdminMixin, AdminTranslation
from mptt.admin import DraggableMPTTAdmin
from django.utils.translation import gettext_lazy as _
from . import models


@admin.register(models.Menu)
class MenuAdmin(SchoolAdminMixin, AdminTranslation, DraggableMPTTAdmin):
    class Media:
        css = {
            "screen": ("css/admin_menu.css",),
        }





@admin.register(models.School)
class SchoolAdmin(DescriptionMixin, SchoolAdminMixin, AdminTranslation):
    list_display = ('name', 'domain', 'created_at', 'updated_at')
    search_fields = ('name', 'domain')
    list_filter = ('created_at', 'updated_at')
    fieldsets = (
        ("Asosiy 📌",
            {"fields": ("is_active", "domain", "name", "slug", "description", "short_description")}
        ),
        ("Raqamlar 📊", {"fields": ("founded_year", "capacity", "student_count", "teacher_count", "direction_count", "class_count")}),
        ("Kontaktlar 📞", {"fields": ("email", "phone_number", "address", "latitude", "longitude")}),
        ("Ijtimoiy tarmoqlar 🔗", {"fields": ("instagram_link", "telegram_link", "facebook_link", "youtube_link")}),
    )
    prepopulated_fields = {
        'slug': ('name',),
    }
    
    def get_readonly_fields(self, request, obj=None):
        ro = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            ro += ["domain"]
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
    list_display = ('image_tag', 'title', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('created_at', 'updated_at')
    list_display_links = ('image_tag', 'title')


@admin.register(models.SchoolLife)
class SchoolLifeAdmin(DescriptionMixin, SchoolAdminMixin, AdminTranslation):
    list_display = ('image_tag', 'title', 'school', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('school', 'created_at', 'updated_at')
    list_display_links = ('image_tag', 'title')