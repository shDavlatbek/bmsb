from rest_framework import serializers
from .models import ResourceVideo, ResourceFile


class ResourceVideoSerializer(serializers.ModelSerializer):
    """Serializer for ResourceVideo model"""
    
    class Meta:
        model = ResourceVideo
        fields = ['id', 'title', 'youtube_link', 'view_count', 'created_at']


class ResourceFileSerializer(serializers.ModelSerializer):
    """Serializer for ResourceFile model"""
    
    file_size = serializers.SerializerMethodField()
    file_extension = serializers.SerializerMethodField()
    
    class Meta:
        model = ResourceFile
        fields = ['id', 'title', 'file', 'download_count', 'file_size', 'file_extension', 'created_at']
    
    def get_file_size(self, obj):
        """Return formatted file size"""
        if obj.file:
            try:
                file_size = obj.file.size
                if file_size < 1024:
                    return f"{file_size} B"
                elif file_size < 1024 * 1024:
                    return f"{file_size / 1024:.1f} KB"
                else:
                    return f"{file_size / (1024 * 1024):.1f} MB"
            except:
                return None
        return None
    
    def get_file_extension(self, obj):
        """Return file extension"""
        if obj.file and obj.file.name:
            return obj.file.name.split('.')[-1].upper() if '.' in obj.file.name else None
        return None 