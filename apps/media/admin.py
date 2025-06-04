from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from apps.common.mixins import SchoolAdminMixin, AdminTranslation, DescriptionMixin
from .models import MediaCollection, MediaImage, MediaVideo


class MediaImageInline(admin.TabularInline):
    """Inline for managing images within a collection"""
    model = MediaImage
    extra = 1
    # fields = ('image', 'show_in_main', 'is_active')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 60px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return ""
    image_preview.short_description = ""


@admin.register(MediaCollection)
class MediaCollectionAdmin(SchoolAdminMixin, AdminTranslation):
    """Admin interface for Media Collections with school scoping and translation support"""
    
    list_display = ('title', 'image_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    ordering = ('-created_at',)
    
    
    inlines = [MediaImageInline]
    
    def image_count(self, obj):
        """Display count of images in collection"""
        count = obj.media_images.count()
        active_count = obj.media_images.filter(is_active=True).count()
        
        if count == active_count:
            return format_html(
                '<span style="color: green; font-weight: bold;">{}</span>',
                count
            )
        else:
            return format_html(
                '<span style="color: orange; font-weight: bold;">{}</span> '
                '<span style="color: gray;">({} ta faol)</span>',
                count, active_count
            )
    image_count.short_description = "Rasmlar"
    image_count.admin_order_field = 'media_images__count'
    
    def get_queryset(self, request):
        """Optimize queryset with prefetch for image counts"""
        qs = super().get_queryset(request)
        return qs.prefetch_related('media_images')



@admin.register(MediaVideo)
class MediaVideoAdmin(AdminTranslation):
    """Admin interface for Media Videos - no school scoping needed as videos are global"""
    
    list_display = ('title', 'youtube_thumbnail', 'is_active', 'created_at')
    list_display_links = ('title',)
    list_filter = ('is_active', 'created_at')
    ordering = ('-created_at',)
    
    readonly_fields = ('video_preview',)
    
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
    
    class Media:
        css = {
            'all': ('css/admin_media.css',)
        }
