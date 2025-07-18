import base64
import hashlib
import hmac
from typing import Optional, Dict, Any
from urllib.parse import quote
from django.conf import settings


class ImgproxyUrlBuilder:
    """
    Generates secure imgproxy URLs for image transformations.
    
    Imgproxy URL format:
    /{signature}/{processing_options}/{encoded_url}.{extension}
    """
    
    def __init__(self):
        self.base_url = settings.IMGPROXY_BASE_URL.rstrip('/')
        self.key = bytes.fromhex(settings.IMGPROXY_KEY)
        self.salt = bytes.fromhex(settings.IMGPROXY_SALT)
        self.enabled = settings.IMGPROXY_ENABLED
        
    def generate_url(
        self,
        image_url: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        resize_type: str = 'fill',
        gravity: str = 'ce',  # center
        enlarge: bool = False,
        extension: Optional[str] = None,
        quality: Optional[int] = None,
        blur: Optional[int] = None,
        sharpen: Optional[float] = None,
        preset: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate imgproxy URL with specified transformations.
        
        Args:
            image_url: Original image URL (can be relative or absolute)
            width: Target width in pixels
            height: Target height in pixels
            resize_type: Resize type (fill, fit, auto, force)
            gravity: Gravity for cropping (no, so, ea, we, ce, sm, etc.)
            enlarge: Allow image enlargement
            extension: Output format (webp, jpg, png, avif)
            quality: Image quality (1-100)
            blur: Blur radius
            sharpen: Sharpen sigma
            preset: Preset name for common transformations
            **kwargs: Additional processing options
            
        Returns:
            Signed imgproxy URL
        """
        
        # If imgproxy is disabled, return original URL
        if not self.enabled:
            return image_url
            
        # Handle presets
        if preset:
            preset_options = self._get_preset_options(preset)
            # Merge preset options with provided options
            for key, value in preset_options.items():
                if key not in locals() or locals()[key] is None:
                    if key == 'width':
                        width = value
                    elif key == 'height':
                        height = value
                    elif key == 'resize_type':
                        resize_type = value
                    elif key == 'quality':
                        quality = value
                    elif key == 'extension':
                        extension = value
        
        # Build processing options
        processing_options = []
        
        # Resize
        if width or height:
            w = width or 0
            h = height or 0
            enlarge_flag = 1 if enlarge else 0
            processing_options.append(f"rs:{resize_type}:{w}:{h}:{enlarge_flag}")
            
        # Gravity
        if gravity and resize_type in ['fill', 'crop']:
            processing_options.append(f"g:{gravity}")
            
        # Quality
        if quality is None:
            quality = settings.IMGPROXY_DEFAULT_QUALITY
        processing_options.append(f"q:{quality}")
        
        # Format
        if extension is None:
            extension = settings.IMGPROXY_DEFAULT_FORMAT
        processing_options.append(f"f:{extension}")
        
        # Blur
        if blur:
            processing_options.append(f"bl:{blur}")
            
        # Sharpen
        if sharpen:
            processing_options.append(f"sh:{sharpen}")
            
        # Smart crop
        if settings.IMGPROXY_ENABLE_SMART_CROP and resize_type == 'fill':
            processing_options.append("sm:1")
            
        # Additional options
        for key, value in kwargs.items():
            if value is not None:
                processing_options.append(f"{key}:{value}")
        
        # Encode source URL
        encoded_url = base64.urlsafe_b64encode(image_url.encode()).decode().rstrip('=')
        
        # Build path
        processing_path = "/".join(processing_options)
        path = f"/{processing_path}/{encoded_url}"
        
        # Generate signature
        signature = self._generate_signature(path)
        
        # Build final URL
        return f"{self.base_url}/{signature}{path}"
    
    def _generate_signature(self, path: str) -> str:
        """Generate HMAC signature for the path."""
        digest = hmac.new(self.key, msg=self.salt + path.encode(), digestmod=hashlib.sha256).digest()
        return base64.urlsafe_b64encode(digest).decode().rstrip('=')
    
    def _get_preset_options(self, preset: str) -> Dict[str, Any]:
        """Get predefined options for common use cases."""
        presets = {
            # Thumbnails
            'thumb_small': {'width': 150, 'height': 150, 'resize_type': 'fill'},
            'thumb_medium': {'width': 300, 'height': 300, 'resize_type': 'fill'},
            'thumb_large': {'width': 500, 'height': 500, 'resize_type': 'fill'},
            
            # List views
            'list_small': {'width': 200, 'height': 150, 'resize_type': 'fill'},
            'list_medium': {'width': 400, 'height': 300, 'resize_type': 'fill'},
            'list_large': {'width': 600, 'height': 450, 'resize_type': 'fill'},
            
            # Banners
            'banner_mobile': {'width': 768, 'height': 400, 'resize_type': 'fill'},
            'banner_desktop': {'width': 1920, 'height': 600, 'resize_type': 'fill'},
            
            # Gallery
            'gallery_thumb': {'width': 250, 'height': 250, 'resize_type': 'fill'},
            'gallery_full': {'width': 1200, 'height': 800, 'resize_type': 'fit'},
            
            # Staff/Teacher photos
            'avatar_small': {'width': 100, 'height': 100, 'resize_type': 'fill', 'gravity': 'ce'},
            'avatar_medium': {'width': 200, 'height': 200, 'resize_type': 'fill', 'gravity': 'ce'},
            'avatar_large': {'width': 400, 'height': 400, 'resize_type': 'fill', 'gravity': 'ce'},
            
            # Icons
            'icon_small': {'width': 64, 'height': 64, 'resize_type': 'fill'},
            'icon_medium': {'width': 128, 'height': 128, 'resize_type': 'fill'},
            
            # High quality
            'hq_medium': {'width': 800, 'quality': 95, 'resize_type': 'fit'},
            'hq_large': {'width': 1600, 'quality': 95, 'resize_type': 'fit'},
            
            # Low bandwidth
            'low_quality': {'quality': 60, 'extension': 'jpg'},
            'very_low_quality': {'quality': 40, 'extension': 'jpg'},
        }
        
        return presets.get(preset, {})
    
    def build_srcset(
        self,
        image_url: str,
        sizes: list[int],
        resize_type: str = 'fill',
        height_ratio: Optional[float] = None,
        **kwargs
    ) -> str:
        """
        Generate srcset attribute for responsive images.
        
        Args:
            image_url: Original image URL
            sizes: List of widths for srcset
            resize_type: Resize type for all sizes
            height_ratio: Height to width ratio (e.g., 0.75 for 4:3)
            **kwargs: Additional options passed to generate_url
            
        Returns:
            Srcset string for use in img tag
        """
        srcset_items = []
        
        for width in sizes:
            height = int(width * height_ratio) if height_ratio else None
            url = self.generate_url(
                image_url,
                width=width,
                height=height,
                resize_type=resize_type,
                **kwargs
            )
            srcset_items.append(f"{url} {width}w")
            
        return ", ".join(srcset_items)


# Global instance
imgproxy = ImgproxyUrlBuilder()


# Convenience functions
def imgproxy_url(image_url: str, **kwargs) -> str:
    """Generate imgproxy URL with specified options."""
    return imgproxy.generate_url(image_url, **kwargs)


def imgproxy_thumbnail(image_url: str, size: str = 'medium') -> str:
    """Generate thumbnail URL using preset sizes."""
    preset = f'thumb_{size}'
    return imgproxy.generate_url(image_url, preset=preset)


def imgproxy_srcset(image_url: str, **kwargs) -> str:
    """Generate srcset for responsive images."""
    default_sizes = [320, 640, 768, 1024, 1280, 1920]
    sizes = kwargs.pop('sizes', default_sizes)
    return imgproxy.build_srcset(image_url, sizes, **kwargs) 