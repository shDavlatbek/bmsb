from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from apps.common.mixins import SchoolAdminMixin, AdminTranslation
from .models import ResourceVideo, ResourceFile


@admin.register(ResourceVideo)
class ResourceVideoAdmin(SchoolAdminMixin, AdminTranslation):
    """Admin interface for Resource Videos with school scoping and translation support"""
    
    list_display = ('title', 'youtube_thumbnail', 'view_count', 'is_active', 'created_at')
    list_display_links = ('title',)
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    ordering = ('-created_at',)
    readonly_fields = ('view_count', 'video_preview')
    
    # fieldsets = (
    #     ('Asosiy ma\'lumotlar 📌', {
    #         'fields': ('title', 'is_active')
    #     }),
    #     ('Video 🎥', {
    #         'fields': ('youtube_link', 'view_count', 'video_preview')
    #     }),
    # )
    
    def youtube_thumbnail(self, obj):
        """Display YouTube video thumbnail"""
        if obj.youtube_link:
            try:
                # Extract video ID from YouTube URL
                import re
                from urllib.parse import urlparse, parse_qs
                
                parsed_url = urlparse(obj.youtube_link)
                if 'youtube.com' in parsed_url.netloc:
                    video_id = parse_qs(parsed_url.query).get('v', [None])[0]
                elif 'youtu.be' in parsed_url.netloc:
                    video_id = parsed_url.path[1:]
                else:
                    return "Noto'g'ri URL"
                
                if video_id:
                    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
                    return format_html(
                        '<img src="{}" style="height: 60px; width: 80px; object-fit: cover; border-radius: 4px;" />',
                        thumbnail_url
                    )
            except:
                pass
        return ""
    youtube_thumbnail.short_description = ""
    
    def video_preview(self, obj):
        """Embed YouTube video preview"""
        if obj.youtube_link:
            try:
                # Extract video ID
                import re
                from urllib.parse import urlparse, parse_qs
                
                parsed_url = urlparse(obj.youtube_link)
                if 'youtube.com' in parsed_url.netloc:
                    video_id = parse_qs(parsed_url.query).get('v', [None])[0]
                elif 'youtu.be' in parsed_url.netloc:
                    video_id = parsed_url.path[1:]
                else:
                    return "Noto'g'ri YouTube havola"
                
                if video_id:
                    return format_html(
                        '<iframe width="320" height="180" src="https://www.youtube.com/embed/{}" '
                        'frameborder="0" allowfullscreen style="border-radius: 8px;"></iframe>',
                        video_id
                    )
            except:
                pass
        return ""
    video_preview.short_description = ""


@admin.register(ResourceFile)
class ResourceFileAdmin(SchoolAdminMixin, AdminTranslation):
    """Admin interface for Resource Files with school scoping and translation support"""
    
    list_display = ('title', 'file_info', 'download_count', 'is_active', 'created_at')
    list_display_links = ('title',)
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    ordering = ('-created_at',)
    readonly_fields = ('download_count', 'file_preview')
    
    def file_info(self, obj):
        """Display file information"""
        if obj.file:
            try:
                file_size = obj.file.size
                if file_size < 1024:
                    size_str = f"{file_size} B"
                elif file_size < 1024 * 1024:
                    size_str = f"{file_size / 1024:.1f} KB"
                else:
                    size_str = f"{file_size / (1024 * 1024):.1f} MB"
                
                file_ext = obj.file.name.split('.')[-1].upper() if '.' in obj.file.name else 'FILE'
                
                return format_html(
                    '<span style="background: #007cba; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{}</span> '
                    '<span style="color: #666;">{}</span>',
                    file_ext, size_str
                )
            except:
                return "Fayl ma'lumoti mavjud emas"
        return ""
    file_info.short_description = "Fayl ma'lumoti"
    
    def file_preview(self, obj):
        """Show file download link"""
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank" style="background: #007cba; color: white; padding: 8px 16px; '
                'text-decoration: none; border-radius: 4px; display: inline-block;">📄 Faylni ko\'rish</a>',
                obj.file.url
            )
        return ""
    file_preview.short_description = ""
