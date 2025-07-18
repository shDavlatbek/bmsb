from rest_framework import serializers
from .imgproxy import imgproxy_url, imgproxy_thumbnail, imgproxy_srcset


class ImgproxyImageField(serializers.ImageField):
    """
    Custom image field that automatically generates imgproxy URLs.
    
    Usage:
        image = ImgproxyImageField(preset='thumb_medium')
        image = ImgproxyImageField(width=300, height=200)
        image = ImgproxyImageField(sizes=[320, 640, 1024])  # For srcset
    """
    
    def __init__(self, **kwargs):
        # Extract imgproxy options
        self.imgproxy_options = {}
        self.generate_srcset = False
        self.srcset_sizes = None
        
        # Extract imgproxy-specific options
        imgproxy_params = [
            'width', 'height', 'resize_type', 'gravity', 'enlarge',
            'extension', 'quality', 'blur', 'sharpen', 'preset'
        ]
        
        for param in imgproxy_params:
            if param in kwargs:
                self.imgproxy_options[param] = kwargs.pop(param)
        
        # Check for srcset generation
        if 'sizes' in kwargs:
            self.generate_srcset = True
            self.srcset_sizes = kwargs.pop('sizes')
            
        super().__init__(**kwargs)
    
    def to_representation(self, value):
        if not value:
            return None
            
        # Get the original URL
        request = self.context.get('request')
        if request:
            url = request.build_absolute_uri(value.url)
        else:
            url = value.url
            
        # If we need srcset, return a dict with url and srcset
        if self.generate_srcset:
            return {
                'url': imgproxy_url(url, **self.imgproxy_options),
                'srcset': imgproxy_srcset(url, sizes=self.srcset_sizes, **self.imgproxy_options)
            }
            
        # Otherwise just return the imgproxy URL
        return imgproxy_url(url, **self.imgproxy_options)


class ImgproxyThumbnailField(serializers.ImageField):
    """
    Simplified field for generating thumbnails with preset sizes.
    
    Usage:
        thumbnail = ImgproxyThumbnailField(size='small')  # small, medium, large
    """
    
    def __init__(self, size='medium', **kwargs):
        self.size = size
        super().__init__(**kwargs)
    
    def to_representation(self, value):
        if not value:
            return None
            
        request = self.context.get('request')
        if request:
            url = request.build_absolute_uri(value.url)
        else:
            url = value.url
            
        return imgproxy_thumbnail(url, size=self.size)


class ResponsiveImageField(serializers.ImageField):
    """
    Field that returns comprehensive responsive image data.
    
    Returns:
    {
        "url": "default imgproxy url",
        "srcset": "responsive srcset string",
        "sizes": "(suggested sizes attribute)",
        "placeholder": "low quality placeholder",
        "original": "original image url"
    }
    """
    
    def __init__(self, default_width=800, sizes=None, **kwargs):
        self.default_width = default_width
        self.sizes = sizes or [320, 640, 768, 1024, 1280, 1920]
        super().__init__(**kwargs)
    
    def to_representation(self, value):
        if not value:
            return None
            
        request = self.context.get('request')
        if request:
            url = request.build_absolute_uri(value.url)
        else:
            url = value.url
            
        return {
            'url': imgproxy_url(url, width=self.default_width, preset='hq_medium'),
            'srcset': imgproxy_srcset(url, sizes=self.sizes),
            'sizes': '(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw',
            'placeholder': imgproxy_url(url, width=50, quality=20, blur=5),
            'original': url
        }


# Mixin for serializers with multiple image fields
class ImgproxySerializerMixin:
    """
    Mixin that provides methods for handling imgproxy URLs in serializers.
    """
    
    def get_imgproxy_url(self, obj, field_name, **options):
        """Generate imgproxy URL for an image field."""
        image = getattr(obj, field_name, None)
        if not image:
            return None
            
        request = self.context.get('request')
        if request:
            url = request.build_absolute_uri(image.url)
        else:
            url = image.url
            
        return imgproxy_url(url, **options)
    
    def get_imgproxy_thumbnail(self, obj, field_name, size='medium'):
        """Generate thumbnail URL for an image field."""
        image = getattr(obj, field_name, None)
        if not image:
            return None
            
        request = self.context.get('request')
        if request:
            url = request.build_absolute_uri(image.url)
        else:
            url = image.url
            
        return imgproxy_thumbnail(url, size=size) 