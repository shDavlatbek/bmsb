from django.contrib import admin
from apps.utils.admin import DescriptionMixin, AdminTranslation
from mptt.admin import DraggableMPTTAdmin
from . import models


@admin.register(models.MenuItem)
class MenuItemAdmin(DraggableMPTTAdmin):
    
    class Media:
        css = {
            "screen": ("css/admin_menu.css",),
        }


@admin.register(models.School)
class SchoolAdmin(DescriptionMixin, AdminTranslation):
    list_display = ('name', 'domain', 'created_at', 'updated_at')
    search_fields = ('name', 'domain')
    list_filter = ('created_at', 'updated_at')
