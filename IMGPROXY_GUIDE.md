# 🖼️ Imgproxy Integration Guide for BMSB

## Overview

Imgproxy has been integrated into the BMSB project to provide on-the-fly image optimization, format conversion, and responsive image delivery. This significantly improves page load times and reduces bandwidth usage.

## 🚀 Quick Start

### 1. Environment Variables

Add these to your `.env` file (defaults are provided for development):

```bash
# Imgproxy Configuration
IMGPROXY_ENABLED=true
IMGPROXY_BASE_URL=http://localhost:8080
IMGPROXY_KEY=943b421c9eb07c830af81030552c86009268de4e532ba2ee2eab8247c6da0881
IMGPROXY_SALT=520f986b998545b4785e0defbc4f3c1203f22de2374a3d53cb7a7fe9fea309c5

# Optional - Override defaults
IMGPROXY_DEFAULT_QUALITY=85
IMGPROXY_DEFAULT_FORMAT=webp
IMGPROXY_ENABLE_SMART_CROP=true
```

**⚠️ IMPORTANT**: For production, generate secure keys:
```bash
# Generate secure key and salt
echo $(xxd -g 2 -l 64 -p /dev/random | tr -d '\n')  # For KEY
echo $(xxd -g 2 -l 64 -p /dev/random | tr -d '\n')  # For SALT
```

### 2. Running with Docker

The imgproxy service is already configured in both `dev.yml` and `prod.yml`:

```bash
# Development
docker-compose -f dev.yml up

# Production
docker-compose -f prod.yml up
```

Imgproxy will be available at:
- Web app: http://localhost:8020 (dev) or http://localhost:8000 (prod)
- Imgproxy: http://localhost:8080

### 3. Testing the Integration

```bash
# Test with a URL
docker-compose exec web python manage.py test_imgproxy --url "http://example.com/image.jpg"

# Test with existing database images
docker-compose exec web python manage.py test_imgproxy
```

## 📝 Usage in Serializers

### Basic Usage - ImgproxyImageField

```python
from apps.common.serializers import ImgproxyImageField

class YourSerializer(serializers.ModelSerializer):
    # Simple optimization with preset
    image = ImgproxyImageField(preset='thumb_medium')
    
    # Custom dimensions
    image = ImgproxyImageField(width=400, height=300, quality=90)
    
    # Multiple versions of same image
    image_desktop = ImgproxyImageField(source='image', preset='banner_desktop')
    image_mobile = ImgproxyImageField(source='image', preset='banner_mobile', read_only=True)
```

### Responsive Images - ResponsiveImageField

```python
from apps.common.serializers import ResponsiveImageField

class BannerSerializer(serializers.ModelSerializer):
    # Returns comprehensive responsive image data
    responsive_image = ResponsiveImageField(source='image')
```

This returns:
```json
{
  "url": "optimized default URL",
  "srcset": "320w, 640w, 1024w, 1920w URLs",
  "sizes": "(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw",
  "placeholder": "low quality blur placeholder",
  "original": "original image URL"
}
```

### Using ImgproxySerializerMixin

```python
from apps.common.serializers import ImgproxySerializerMixin

class YourSerializer(ImgproxySerializerMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    def get_image_url(self, obj):
        # Use mixin method
        return self.get_imgproxy_url(obj, 'image', width=400, height=300)
```

## 🎨 Available Presets

### Thumbnails
- `thumb_small`: 150x150 (fill)
- `thumb_medium`: 300x300 (fill)
- `thumb_large`: 500x500 (fill)

### List Views
- `list_small`: 200x150 (fill)
- `list_medium`: 400x300 (fill)
- `list_large`: 600x450 (fill)

### Banners
- `banner_mobile`: 768x400 (fill)
- `banner_desktop`: 1920x600 (fill)

### Gallery
- `gallery_thumb`: 250x250 (fill)
- `gallery_full`: 1200x800 (fit)

### Avatars
- `avatar_small`: 100x100 (fill, centered)
- `avatar_medium`: 200x200 (fill, centered)
- `avatar_large`: 400x400 (fill, centered)

### Icons
- `icon_small`: 64x64 (fill)
- `icon_medium`: 128x128 (fill)

### Quality Presets
- `hq_medium`: 800px width, 95 quality
- `hq_large`: 1600px width, 95 quality
- `low_quality`: 60 quality, jpg
- `very_low_quality`: 40 quality, jpg

## 🔧 Direct Usage in Views/Templates

```python
from apps.common.imgproxy import imgproxy_url, imgproxy_thumbnail

# In a view
def get_optimized_url(image_path):
    return imgproxy_url(image_path, width=800, height=600, quality=85)

# Get thumbnail
thumbnail = imgproxy_thumbnail(image_path, size='medium')

# Generate srcset for responsive images
from apps.common.imgproxy import imgproxy_srcset
srcset = imgproxy_srcset(image_path, sizes=[320, 640, 1024])
```

## 🌐 Frontend Integration

### React/Next.js Example

```jsx
// Simple image
<img 
  src={data.image} 
  alt={data.title}
  loading="lazy"
/>

// Responsive image with srcset
<img 
  src={data.responsive_image.url}
  srcset={data.responsive_image.srcset}
  sizes={data.responsive_image.sizes}
  alt={data.title}
  loading="lazy"
/>

// With placeholder blur
<div style={{ position: 'relative' }}>
  <img 
    src={data.responsive_image.placeholder}
    style={{ filter: 'blur(20px)', position: 'absolute' }}
  />
  <img 
    src={data.responsive_image.url}
    srcset={data.responsive_image.srcset}
    sizes={data.responsive_image.sizes}
    onLoad={(e) => e.target.previousSibling.remove()}
  />
</div>
```

### Picture Element for Art Direction

```jsx
<picture>
  <source media="(max-width: 768px)" srcset={data.image_mobile} />
  <source media="(min-width: 769px)" srcset={data.image_desktop} />
  <img src={data.image} alt={data.title} />
</picture>
```

## 📊 Performance Benefits

1. **Automatic Format Selection**: Serves WebP/AVIF to supported browsers
2. **Responsive Images**: Different sizes for different devices
3. **Lazy Loading**: Combined with browser lazy loading
4. **Quality Optimization**: Balanced quality vs file size
5. **Smart Cropping**: AI-based cropping for better compositions
6. **Caching**: Processed images are cached (30 days by default)

## 🔒 Security

- All URLs are cryptographically signed to prevent abuse
- Only authorized transformations are allowed
- Source images are served read-only
- No arbitrary file access

## 🛠️ Advanced Configuration

### Custom Processing Options

```python
# Blur effect
blurred = imgproxy_url(image, blur=10)

# Sharpen
sharp = imgproxy_url(image, sharpen=0.5)

# Grayscale
grayscale = imgproxy_url(image, saturation=0)

# Custom gravity
centered = imgproxy_url(image, width=200, height=200, gravity='ce')
```

### Gravity Options
- `no`: north (top edge)
- `so`: south (bottom edge)
- `ea`: east (right edge)
- `we`: west (left edge)
- `ce`: center
- `sm`: smart (AI-based)

### Resize Types
- `fill`: Fill the area, crop if needed
- `fit`: Fit within bounds, maintain aspect ratio
- `auto`: Choose automatically
- `force`: Force exact dimensions

## 🐛 Troubleshooting

### Images not optimizing
1. Check if `IMGPROXY_ENABLED=true` in settings
2. Verify imgproxy service is running: `docker-compose ps`
3. Check imgproxy logs: `docker-compose logs imgproxy`

### Invalid signature errors
- Ensure KEY and SALT match in Django settings and imgproxy environment

### CORS issues
- Imgproxy serves proper CORS headers by default
- If issues persist, check nginx configuration

### Testing URLs
```bash
# Test if imgproxy is working
curl http://localhost:8080/

# Test a signed URL (use output from test_imgproxy command)
curl "http://localhost:8080/[signed-url]" -o test.webp
```

## 📈 Monitoring

Monitor imgproxy performance:
```bash
# View imgproxy logs
docker-compose logs -f imgproxy

# Check memory usage
docker stats bmsb-imgproxy
```

## 🔄 Migration Guide

To migrate existing serializers:

1. Import imgproxy fields:
   ```python
   from apps.common.serializers import ImgproxyImageField
   ```

2. Replace ImageField:
   ```python
   # Before
   image = serializers.ImageField()
   
   # After
   image = ImgproxyImageField(preset='appropriate_preset')
   ```

3. Test API responses to ensure URLs are generated correctly

## 📚 Additional Resources

- [Imgproxy Documentation](https://docs.imgproxy.net/)
- [WebP Support](https://caniuse.com/webp)
- [Responsive Images Guide](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images) 