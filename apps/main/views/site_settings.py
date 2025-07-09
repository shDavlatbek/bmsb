from rest_framework.generics import RetrieveAPIView
from ..models import SiteSettings
from ..serializers.site_settings import SiteSettingsSerializer


class SiteSettingsView(RetrieveAPIView):
    serializer_class = SiteSettingsSerializer
    
    def get_object(self):
        # Get the first SiteSettings instance, or create one if it doesn't exist
        obj, created = SiteSettings.objects.get_or_create(id=1)
        return obj 