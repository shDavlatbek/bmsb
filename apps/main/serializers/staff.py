from rest_framework import serializers
from ..models import Staff


class StaffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = [
            'id', 'full_name', 'slug', 'position', 'image', 
            'instagram_link', 'telegram_link', 'facebook_link', 'linkedin_link',
            'experience_years', 'created_at'
        ] 