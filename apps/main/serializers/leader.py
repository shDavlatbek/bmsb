from rest_framework import serializers
from ..models import Leader


class LeaderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leader
        fields = [
            'id', 'full_name', 'slug', 'position', 'image', 
            'working_days', 'created_at'
        ]


class LeaderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leader
        fields = [
            'id', 'full_name', 'slug', 'position', 'image', 'description',
            'phone_number', 'email', 'instagram_link', 'telegram_link',
            'facebook_link', 'linkedin_link', 'working_days', 'created_at'
        ] 