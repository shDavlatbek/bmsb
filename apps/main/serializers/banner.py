from rest_framework import serializers
from apps.main.models import Banner


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'image', 'button_text', 'link', 'is_active'] 