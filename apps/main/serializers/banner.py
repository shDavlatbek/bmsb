from rest_framework import serializers
from apps.main.models import Banner
from apps.common.serializers import ImgproxyImageField, ResponsiveImageField


class BannerSerializer(serializers.ModelSerializer):
    # Provide optimized image URL with imgproxy
    image = ImgproxyImageField(preset='banner_desktop')
    
    # For mobile optimization
    image_mobile = ImgproxyImageField(source='image', preset='banner_mobile', read_only=True)
    
    # Responsive image data with srcset
    responsive_image = ResponsiveImageField(source='image', read_only=True)
    
    class Meta:
        model = Banner
        fields = ['id', 'title', 'image', 'image_mobile', 'responsive_image', 'button_text', 'link'] 