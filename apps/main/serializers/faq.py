from rest_framework import serializers
from apps.main.models import FAQ


class FAQListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'title', 'description'] 