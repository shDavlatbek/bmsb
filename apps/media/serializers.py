from rest_framework import serializers
from .models import MediaCollection, MediaImage, MediaVideo


class MediaImageSerializer(serializers.ModelSerializer):
    """Serializer for MediaImage model"""
    
    class Meta:
        model = MediaImage
        fields = ['id', 'image', 'show_in_main', 'created_at']


class MediaCollectionListSerializer(serializers.ModelSerializer):
    """
    Serializer for MediaCollection list view.
    Returns first show_in_main image or first image if no show_in_main exists.
    """
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = MediaCollection
        fields = ['id', 'title', 'slug', 'image', 'created_at']
    
    def get_image(self, obj):
        """
        Return first show_in_main image URL, otherwise first image URL, or None if no images.
        """
        # Use the prefetched ordered_images from the view
        if hasattr(obj, 'ordered_images') and obj.ordered_images:
            # ordered_images is already sorted by -show_in_main, id
            first_image = obj.ordered_images[0]
            if first_image.image:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(first_image.image.url)
                return first_image.image.url
        return None


class MediaCollectionDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for MediaCollection detail view.
    Returns collection info and all associated MediaImages.
    """
    media_images = MediaImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = MediaCollection
        fields = ['id', 'title', 'slug', 'created_at', 'media_images']


class MediaVideoSerializer(serializers.ModelSerializer):
    """Serializer for MediaVideo model"""
    
    class Meta:
        model = MediaVideo
        fields = ['id', 'title', 'youtube_link', 'created_at'] 