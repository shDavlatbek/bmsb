from rest_framework import serializers
from apps.main.models import SchoolLife


class SchoolLifeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolLife
        fields = ['id', 'image', 'title', 'description'] 