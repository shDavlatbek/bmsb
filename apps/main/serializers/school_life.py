from rest_framework import serializers
from apps.main.models import SchoolLife


class SchoolLifeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolLife
        fields = ['id', 'school', 'image', 'title', 'description', 'is_active', 'created_at', 'updated_at'] 