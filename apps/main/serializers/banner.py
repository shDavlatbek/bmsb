from rest_framework import serializers
from apps.main.models import Banner


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['title', 'image', 'button_text', 'link'] 