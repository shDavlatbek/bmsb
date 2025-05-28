import re
from rest_framework import serializers
from apps.news.models import News, Category
from django.utils.html import strip_tags

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class NewsListSerializer(serializers.ModelSerializer):
    """Serializer for listing news with basic fields"""
    category = CategorySerializer(read_only=True)
    content = serializers.SerializerMethodField()
    
    def get_content(self, obj):
        cleaned = re.sub(r'[\r\n]+', ' ', obj.content).strip()
        return strip_tags(cleaned[:100] + '...')
    
    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'image', 'content', 'category', 'view_count', 'created_at']


class NewsDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed news view with all fields"""
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'image', 'category', 'content', 'view_count', 'created_at', 'updated_at']


 