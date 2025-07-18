from rest_framework import serializers
from ..models import Staff
from apps.common.serializers import ImgproxyImageField


class StaffListSerializer(serializers.ModelSerializer):
    # Optimized avatar image with imgproxy
    image = ImgproxyImageField(preset='avatar_medium')
    
    # Thumbnail for smaller displays
    image_thumbnail = ImgproxyImageField(source='image', preset='avatar_small', read_only=True)
    
    class Meta:
        model = Staff
        fields = [
            'id', 'full_name', 'slug', 'position', 'image', 'image_thumbnail',
            'instagram_link', 'telegram_link', 'facebook_link', 'linkedin_link',
            'experience_years', 'created_at'
        ] 