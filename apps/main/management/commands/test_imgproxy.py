from django.core.management.base import BaseCommand
from django.conf import settings
from apps.common.imgproxy import build_imgproxy_url, get_thumbnail_url, get_preset_url, get_responsive_url
from apps.main.models import Banner, Staff, Teacher


class Command(BaseCommand):
    help = 'Test imgproxy URL generation in insecure mode'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            help='Test with a specific image URL',
        )
        parser.add_argument(
            '--base-url',
            type=str,
            default='http://localhost:8080',
            help='Imgproxy base URL',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n🔍 Testing Imgproxy Integration (Insecure Mode)\n'))
        
        base_url = options['base_url']
        
        # Check if imgproxy is running
        self.stdout.write(f"Imgproxy Base URL: {base_url}")
        self.stdout.write("Mode: Insecure (no signature required)")
        self.stdout.write("")

        # Test with provided URL
        if options['url']:
            test_url = options['url']
            self.stdout.write(self.style.MIGRATE_HEADING(f"\n📷 Testing with URL: {test_url}"))
            self._test_url_generation(test_url, base_url)
            return

        # Test with actual model data
        self._test_with_models(base_url)

    def _test_url_generation(self, source_url, base_url):
        """Test various imgproxy URL generation methods"""
        
        # Initialize imgproxy with custom base URL
        from apps.common.imgproxy import SimpleImgproxyUrlBuilder
        imgproxy = SimpleImgproxyUrlBuilder(base_url)
        
        # Basic resize
        basic_url = imgproxy.build_url(source_url, width=300, height=200)
        self.stdout.write(f"\n✅ Basic resize (300x200):")
        self.stdout.write(f"   {basic_url}")
        
        # Different resize types
        self.stdout.write(f"\n✅ Resize types:")
        resize_types = ['fit', 'fill', 'crop']
        for resize_type in resize_types:
            url = imgproxy.build_url(source_url, width=400, height=300, resize_type=resize_type)
            self.stdout.write(f"   {resize_type}: {url}")
        
        # Thumbnail sizes
        self.stdout.write(f"\n✅ Thumbnail presets:")
        thumb_sizes = [100, 200, 300]
        for size in thumb_sizes:
            url = imgproxy.build_url(source_url, width=size, height=size, resize_type='fill', quality=85)
            self.stdout.write(f"   {size}x{size}: {url}")
        
        # Quality variations
        self.stdout.write(f"\n✅ Quality variations:")
        qualities = [50, 75, 85, 95]
        for quality in qualities:
            url = imgproxy.build_url(source_url, width=400, quality=quality)
            self.stdout.write(f"   Q{quality}: {url}")
        
        # Format variations
        self.stdout.write(f"\n✅ Format variations:")
        formats = ['webp', 'jpg', 'png']
        for fmt in formats:
            url = imgproxy.build_url(source_url, width=400, format=fmt)
            self.stdout.write(f"   {fmt}: {url}")
            
        # Custom processing options
        self.stdout.write(f"\n✅ Advanced options:")
        blur_url = imgproxy.build_url(source_url, width=300, bl=5)  # blur
        sharp_url = imgproxy.build_url(source_url, width=300, sh=1)  # sharpen
        bw_url = imgproxy.build_url(source_url, width=300, saturation=0)  # black & white
        self.stdout.write(f"   Blur: {blur_url}")
        self.stdout.write(f"   Sharpen: {sharp_url}")
        self.stdout.write(f"   B&W: {bw_url}")
        
        # Frontend-style URL construction
        self.stdout.write(f"\n✅ Frontend-style URL construction:")
        manual_url = f"{base_url}/insecure/rs:fit:128:128:0/q:100/plain/{source_url}"
        self.stdout.write(f"   Manual: {manual_url}")

    def _test_with_models(self, base_url):
        """Test with actual model instances"""
        
        from apps.common.imgproxy import SimpleImgproxyUrlBuilder
        imgproxy = SimpleImgproxyUrlBuilder(base_url)
        
        # Test with Banner
        banner = Banner.objects.filter(image__isnull=False).first()
        if banner:
            self.stdout.write(self.style.MIGRATE_HEADING(f"\n📷 Testing with Banner: {banner.title}"))
            if banner.image:
                url = f"http://localhost:8000{banner.image.url}"
                self.stdout.write(f"Source: {url}")
                
                # Banner presets
                desktop = imgproxy.build_url(url, width=1920, height=600, resize_type='fill')
                mobile = imgproxy.build_url(url, width=768, height=400, resize_type='fill')
                self.stdout.write(f"Desktop: {desktop}")
                self.stdout.write(f"Mobile: {mobile}")
        
        # Test with Staff
        staff = Staff.objects.filter(image__isnull=False).first()
        if staff:
            self.stdout.write(self.style.MIGRATE_HEADING(f"\n📷 Testing with Staff: {staff.full_name}"))
            if staff.image:
                url = f"http://localhost:8000{staff.image.url}"
                self.stdout.write(f"Source: {url}")
                
                # Avatar presets
                avatar_sizes = [100, 200, 400]
                for size in avatar_sizes:
                    avatar_url = imgproxy.build_url(url, width=size, height=size, resize_type='fill')
                    self.stdout.write(f"Avatar {size}x{size}: {avatar_url}")
        
        if not any([banner, staff]):
            self.stdout.write(self.style.WARNING("\n⚠️  No models with images found in database"))
            self.stdout.write("   Try uploading some images through admin first")
            self.stdout.write("   Or use --url option to test with a specific URL")
            
        # Example URLs for frontend integration
        self.stdout.write(self.style.MIGRATE_HEADING("\n🌐 Frontend Integration Examples:"))
        example_url = "https://cdn.lamenu.uz/files/photo/example.jpg"
        
        self.stdout.write(f"\nJavaScript/React examples:")
        self.stdout.write(f"const thumbnailUrl = `{base_url}/insecure/rs:fill:200:200:0/q:85/plain/${{imageUrl}}`;")
        self.stdout.write(f"const responsiveUrl = `{base_url}/insecure/rs:fit:${{width}}:0:0/q:85/plain/${{imageUrl}}`;")
        
        self.stdout.write(f"\nDirect URL examples:")
        thumb_example = f"{base_url}/insecure/rs:fill:200:200:0/q:85/plain/{example_url}"
        responsive_example = f"{base_url}/insecure/rs:fit:800:0:0/q:85/plain/{example_url}"
        self.stdout.write(f"Thumbnail: {thumb_example}")
        self.stdout.write(f"Responsive: {responsive_example}")
        
        self.stdout.write(f"\nYour production URL format:")
        prod_example = f"https://ipx.lamenu.uz/insecure/rs:fit:128:128:0/q:100/plain/{example_url}"
        self.stdout.write(f"Production: {prod_example}") 