from rest_framework import serializers
from ..models import Document, DocumentCategory


class DocumentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentCategory
        fields = ['id', 'name']


class DocumentSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Document
        fields = [
            'id', 'title', 'file', 'category', 'category_name', 'created_at'
        ] 