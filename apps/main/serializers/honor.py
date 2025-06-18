from rest_framework import serializers
from django.utils.html import strip_tags
from apps.main.models import Honors, HonorAchievements


class HonorAchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HonorAchievements
        fields = ['id', 'year', 'description', 'address', 'created_at']


class HonorsListSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    type_text = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Honors
        fields = ['id', 'full_name', 'slug', 'type', 'type_text', 'image', 'description', 'created_at']
    
    def get_description(self, obj):
        """Strip HTML tags and truncate to 100 characters"""
        if obj.description:
            plain_text = strip_tags(obj.description)
            return plain_text[:100] + '...' if len(plain_text) > 100 else plain_text
        return ''


class HonorsDetailSerializer(serializers.ModelSerializer):
    achievements = HonorAchievementsSerializer(many=True, read_only=True)
    type_text = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Honors
        fields = [
            'id', 'full_name', 'slug', 'type', 'type_text', 'description', 'image',
            'email', 'phone_number', 'achievements', 'created_at'
        ] 