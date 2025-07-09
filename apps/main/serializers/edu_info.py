from rest_framework import serializers
from ..models import EduInfo


class EduInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EduInfo
        fields = ['id', 'title', 'description', 'created_at'] 