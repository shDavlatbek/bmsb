from rest_framework import serializers
from .models import MediaCollection, MediaImage, MediaVideo
from apps.common.serializers import ImgproxyImageField, ResponsiveImageField, ImgproxySerializerMixin


class MediaImageSerializer(serializers.ModelSerializer):
    """Serializer for MediaImage model with imgproxy optimization"""
    
    # Gallery thumbnail
    image = ImgproxyImageField(preset='gallery_thumb')
    
    # Full responsive image data for lightbox/modal
    full_image = ResponsiveImageField(source='image', read_only=True)
    
    class Meta:
        model = MediaImage
        fields = ['id', 'image', 'full_image', 'show_in_main', 'created_at']


class MediaCollectionListSerializer(ImgproxySerializerMixin, serializers.ModelSerializer):
    """
    Serializer for MediaCollection list view.
    Returns first show_in_main image or first image if no show_in_main exists.
    """
    image = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    
    class Meta: 
        model = MediaCollection
        fields = ['id', 'title', 'slug', 'image', 'count', 'created_at']
    
    def get_image(self, obj):
        """
        Return first show_in_main image URL with imgproxy optimization, 
        otherwise first image URL, or None if no images.
        """
        # Use the prefetched ordered_images from the view
        if hasattr(obj, 'ordered_images') and obj.ordered_images:
            # ordered_images is already sorted by -show_in_main, id
            first_image = obj.ordered_images[0]
            if first_image.image:
                request = self.context.get('request')
                if request:
                    url = request.build_absolute_uri(first_image.image.url)
                else:
                    url = first_image.image.url
                
                # Return imgproxy optimized URL
                from apps.common.imgproxy import imgproxy_url
                return imgproxy_url(url, preset='list_medium')
        return None

    def get_count(self, obj):
        """
        Return the total number of images in this collection.
        """
        # Use the prefetched ordered_images if available, otherwise count from the database
        if hasattr(obj, 'ordered_images'):
            return len(obj.ordered_images)
        return obj.media_images.count()


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