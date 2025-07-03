from rest_framework import serializers
from ..models import Comments


class CommentsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'image', 'full_name', 'rating', 'comment', 'created_at']


class CommentsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'image', 'full_name', 'rating', 'comment', 'created_at'] 