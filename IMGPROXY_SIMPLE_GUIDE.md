# 🖼️ Imgproxy Simple Setup for BMSB

## Overview

This is a simplified imgproxy setup for frontend-direct usage. The imgproxy service runs in insecure mode and frontend applications construct URLs directly.

## 🚀 Quick Setup

### 1. Environment Variables (Optional)

Add to your `.env` file if you want to customize:

```bash
# Optional - Customize allowed sources
IMGPROXY_ALLOWED_SOURCES=cdn.lamenu.uz,localhost,127.0.0.1

# Optional - Customize worker count for production
IMGPROXY_WORKERS=4
```

### 2. Start Services

```bash
# Development
docker-compose -f dev.yml up

# Production  
docker-compose -f prod.yml up
```

Imgproxy will be available at:
- Development: http://localhost:8080
- Production: Proxied via nginx to https://ipx.lamenu.uz

### 3. Test the Setup

```bash
# Test imgproxy service
docker-compose exec web python manage.py test_imgproxy

# Test with custom URL
docker-compose exec web python manage.py test_imgproxy --url "https://cdn.lamenu.uz/image.jpg"

# Test with custom base URL (if proxied)
docker-compose exec web python manage.py test_imgproxy --base-url "https://ipx.lamenu.uz"
```

## 🌐 Frontend Usage

### URL Format

```
https://ipx.lamenu.uz/insecure/{processing_options}/plain/{source_image_url}
```

### Basic Examples

```javascript
// Base URL (change for your setup)
const IMGPROXY_BASE = 'https://ipx.lamenu.uz';

// Thumbnail 200x200, fill, quality 85
const thumbnailUrl = `${IMGPROXY_BASE}/insecure/rs:fill:200:200:0/q:85/plain/${sourceImageUrl}`;

// Responsive width 800px, fit, quality 85  
const responsiveUrl = `${IMGPROXY_BASE}/insecure/rs:fit:800:0:0/q:85/plain/${sourceImageUrl}`;

// High quality 1200px width
const highQualityUrl = `${IMGPROXY_BASE}/insecure/rs:fit:1200:0:0/q:95/plain/${sourceImageUrl}`;

// Mobile banner 768x400
const mobileBannerUrl = `${IMGPROXY_BASE}/insecure/rs:fill:768:400:0/q:85/plain/${sourceImageUrl}`;
```

### Processing Options

| Option | Format | Description | Example |
|--------|--------|-------------|---------|
| Resize | `rs:{type}:{width}:{height}:{enlarge}` | Resize image | `rs:fit:800:600:0` |
| Quality | `q:{quality}` | JPEG quality 1-100 | `q:85` |
| Format | `f:{format}` | Output format | `f:webp` |
| Blur | `bl:{radius}` | Blur effect | `bl:5` |
| Sharpen | `sh:{sigma}` | Sharpen effect | `sh:1` |
| Saturation | `saturation:{value}` | Color saturation | `saturation:0` (B&W) |

### Resize Types

- `fit`: Fit within bounds, maintain aspect ratio
- `fill`: Fill area exactly, crop if needed  
- `crop`: Crop to exact dimensions
- `force`: Force exact dimensions (may distort)

### React Hook Example

```javascript
import { useMemo } from 'react';

const useImgProxy = (sourceUrl, options = {}) => {
  const { 
    width = 400, 
    height = 0, 
    type = 'fit', 
    quality = 85, 
    enlarge = 0 
  } = options;

  return useMemo(() => {
    if (!sourceUrl) return null;
    
    const IMGPROXY_BASE = process.env.NEXT_PUBLIC_IMGPROXY_URL || 'https://ipx.lamenu.uz';
    const processing = `rs:${type}:${width}:${height}:${enlarge}/q:${quality}`;
    
    return `${IMGPROXY_BASE}/insecure/${processing}/plain/${sourceUrl}`;
  }, [sourceUrl, width, height, type, quality, enlarge]);
};

// Usage
function ImageComponent({ src, alt }) {
  const thumbnailUrl = useImgProxy(src, { width: 300, height: 300, type: 'fill' });
  
  return <img src={thumbnailUrl} alt={alt} loading="lazy" />;
}
```

### Responsive Images

```javascript
// Generate srcset for responsive images
function generateSrcSet(sourceUrl, sizes = [320, 640, 768, 1024, 1280, 1920]) {
  const IMGPROXY_BASE = 'https://ipx.lamenu.uz';
  
  return sizes
    .map(width => {
      const url = `${IMGPROXY_BASE}/insecure/rs:fit:${width}:0:0/q:85/plain/${sourceUrl}`;
      return `${url} ${width}w`;
    })
    .join(', ');
}

// Usage in React
function ResponsiveImage({ src, alt }) {
  const srcSet = generateSrcSet(src);
  const defaultSrc = useImgProxy(src, { width: 800 });
  
  return (
    <img 
      src={defaultSrc}
      srcSet={srcSet}
      sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
      alt={alt}
      loading="lazy"
    />
  );
}
```

### Next.js Image Component

```javascript
import Image from 'next/image';

function OptimizedImage({ src, width, height, alt, className }) {
  const imgproxyLoader = ({ src, width, quality }) => {
    const q = quality || 85;
    return `https://ipx.lamenu.uz/insecure/rs:fit:${width}:0:0/q:${q}/plain/${src}`;
  };

  return (
    <Image
      loader={imgproxyLoader}
      src={src}
      width={width}
      height={height}
      alt={alt}
      className={className}
      quality={85}
    />
  );
}
```

## 🔧 Nginx Proxy Configuration

If you're proxying imgproxy through nginx to `https://ipx.lamenu.uz`:

```nginx
upstream imgproxy {
    server localhost:8080;
}

server {
    listen 443 ssl http2;
    server_name ipx.lamenu.uz;
    
    # SSL configuration here...
    
    location / {
        proxy_pass http://imgproxy;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Cache processed images
        proxy_cache imgproxy_cache;
        proxy_cache_valid 200 1d;
        proxy_cache_use_stale error timeout invalid_header updating;
        proxy_cache_lock on;
        
        # Add cache headers
        add_header X-Cache-Status $upstream_cache_status;
    }
}

# Cache zone
proxy_cache_path /var/cache/nginx/imgproxy levels=1:2 keys_zone=imgproxy_cache:10m max_size=1g inactive=1d use_temp_path=off;
```

## 📊 Performance Tips

1. **Use appropriate quality**: 85 for most images, 95 for high-quality, 70 for thumbnails
2. **Choose right resize type**: 
   - `fit` for responsive images
   - `fill` for exact dimensions (avatars, thumbnails)
3. **WebP format**: Let imgproxy auto-detect format based on Accept headers
4. **Lazy loading**: Always use `loading="lazy"` on images
5. **Responsive images**: Use srcset for different screen sizes

## 🚨 Security Considerations

- **Allowed sources**: Only whitelisted domains can be processed
- **File size limits**: Max 50MB source files
- **Insecure mode**: No signature required (simpler but less secure)
- **Rate limiting**: Consider adding rate limiting in nginx

## 🐛 Troubleshooting

### Service not starting
```bash
# Check service status
docker-compose ps

# Check imgproxy logs  
docker-compose logs imgproxy

# Test imgproxy directly
curl http://localhost:8080/health
```

### Invalid source URL
- Check if source domain is in `IMGPROXY_ALLOWED_SOURCES`
- Ensure source URL is accessible
- Verify URL encoding if special characters

### Poor performance
- Check if nginx caching is enabled
- Monitor Docker resource usage
- Increase `IMGPROXY_WORKERS` for production

## 📚 Reference

- [Imgproxy Documentation](https://docs.imgproxy.net/)
- [Processing Options](https://docs.imgproxy.net/usage/processing)
- [Configuration](https://docs.imgproxy.net/configuration)

Your example URL format:
```
https://ipx.lamenu.uz/insecure/rs:fit:128:128:0/q:100/plain/https://cdn.lamenu.uz/files/photo/2e4d035f-3f18-4204-aeec-f175b5af3085/f1de160d-df1b-4c59-a1be-ca1f5805ba50.webp
```

This creates a 128x128 fitted image with 100% quality from the source URL. 