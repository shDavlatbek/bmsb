from django.core.management.base import BaseCommand
from django.conf import settings
from apps.common.imgproxy import imgproxy, imgproxy_url, imgproxy_thumbnail, imgproxy_srcset
from apps.main.models import Banner, Staff, Teacher


class Command(BaseCommand):
    help = 'Test imgproxy URL generation'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            help='Test with a specific image URL',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n🔍 Testing Imgproxy Integration\n'))
        
        # Check configuration
        self.stdout.write(f"Imgproxy Enabled: {settings.IMGPROXY_ENABLED}")
        self.stdout.write(f"Imgproxy Base URL: {settings.IMGPROXY_BASE_URL}")
        self.stdout.write(f"Default Quality: {settings.IMGPROXY_DEFAULT_QUALITY}")
        self.stdout.write(f"Default Format: {settings.IMGPROXY_DEFAULT_FORMAT}")
        self.stdout.write("")

        # Test with provided URL
        if options['url']:
            test_url = options['url']
            self.stdout.write(self.style.MIGRATE_HEADING(f"\n📷 Testing with URL: {test_url}"))
            self._test_url_generation(test_url)
            return

        # Test with actual model data
        self._test_with_models()

    def _test_url_generation(self, url):
        """Test various imgproxy URL generation methods"""
        
        # Basic URL
        basic_url = imgproxy_url(url, width=300, height=200)
        self.stdout.write(f"\n✅ Basic resize (300x200):")
        self.stdout.write(f"   {basic_url}")
        
        # Thumbnail presets
        self.stdout.write(f"\n✅ Thumbnail presets:")
        for size in ['small', 'medium', 'large']:
            thumb_url = imgproxy_thumbnail(url, size=size)
            self.stdout.write(f"   {size}: {thumb_url}")
        
        # Banner presets
        self.stdout.write(f"\n✅ Banner presets:")
        banner_desktop = imgproxy_url(url, preset='banner_desktop')
        banner_mobile = imgproxy_url(url, preset='banner_mobile')
        self.stdout.write(f"   Desktop: {banner_desktop}")
        self.stdout.write(f"   Mobile: {banner_mobile}")
        
        # Srcset generation
        self.stdout.write(f"\n✅ Responsive srcset:")
        srcset = imgproxy_srcset(url, sizes=[320, 640, 1024, 1920])
        for item in srcset.split(', '):
            self.stdout.write(f"   {item}")
        
        # Quality variations
        self.stdout.write(f"\n✅ Quality variations:")
        high_quality = imgproxy_url(url, width=800, quality=95)
        low_quality = imgproxy_url(url, width=800, quality=40)
        self.stdout.write(f"   High quality: {high_quality}")
        self.stdout.write(f"   Low quality: {low_quality}")
        
        # Format variations
        self.stdout.write(f"\n✅ Format variations:")
        for fmt in ['webp', 'jpg', 'png']:
            format_url = imgproxy_url(url, width=400, extension=fmt)
            self.stdout.write(f"   {fmt}: {format_url}")

    def _test_with_models(self):
        """Test with actual model instances"""
        
        # Test with Banner
        banner = Banner.objects.filter(image__isnull=False).first()
        if banner:
            self.stdout.write(self.style.MIGRATE_HEADING(f"\n📷 Testing with Banner: {banner.title}"))
            if banner.image:
                url = f"http://localhost:8000{banner.image.url}"
                self._test_url_generation(url)
            else:
                self.stdout.write(self.style.WARNING("   No image found"))
        
        # Test with Staff
        staff = Staff.objects.filter(image__isnull=False).first()
        if staff:
            self.stdout.write(self.style.MIGRATE_HEADING(f"\n📷 Testing with Staff: {staff.full_name}"))
            if staff.image:
                url = f"http://localhost:8000{staff.image.url}"
                # Test avatar presets
                self.stdout.write(f"\n✅ Avatar presets:")
                for size in ['small', 'medium', 'large']:
                    avatar_url = imgproxy_url(url, preset=f'avatar_{size}')
                    self.stdout.write(f"   {size}: {avatar_url}")
        
        # Test with Teacher
        teacher = Teacher.objects.filter(image__isnull=False).first()
        if teacher:
            self.stdout.write(self.style.MIGRATE_HEADING(f"\n📷 Testing with Teacher: {teacher.full_name}"))
            if teacher.image:
                url = f"http://localhost:8000{teacher.image.url}"
                # Test list view presets
                self.stdout.write(f"\n✅ List view presets:")
                for size in ['small', 'medium', 'large']:
                    list_url = imgproxy_url(url, preset=f'list_{size}')
                    self.stdout.write(f"   {size}: {list_url}")
        
        if not any([banner, staff, teacher]):
            self.stdout.write(self.style.WARNING("\n⚠️  No models with images found in database"))
            self.stdout.write("   Try uploading some images through admin first")
            self.stdout.write("   Or use --url option to test with a specific URL") 