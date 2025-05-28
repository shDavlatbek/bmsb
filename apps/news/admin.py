from django.contrib import admin
from apps.common.mixins import SchoolAdminMixin, AdminTranslation, DescriptionMixin
from apps.news.models import News, Category


@admin.register(Category)
class CategoryAdmin(SchoolAdminMixin, AdminTranslation):
    list_display = ['name', 'is_active']
    
    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(News)
class NewsAdmin(SchoolAdminMixin, DescriptionMixin, AdminTranslation):
    list_display = ['image_tag', 'title', 'category', 'view_count', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    list_display_links = ['image_tag', 'title']
    prepopulated_fields = {
        'slug': ('title',),
    }
    
    # search_fields = ['title', 'description']
    readonly_fields = ['view_count']
    # fieldsets = (
    #     (None, {
    #         'fields': ('school', 'category', 'title', 'slug', 'image')
    #     }),
    #     ('Kontent', {
    #         'fields': ('description',)
    #     }),
    # )
    
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.select_related('school', 'category')
