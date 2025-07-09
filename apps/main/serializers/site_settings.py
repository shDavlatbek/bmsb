from rest_framework import serializers
from ..models import SiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = (
            'school_life', 'directions', 'numbers', 'teachers', 'honors', 'news', 
            'gallery', 'contact', 'comments', 'faqs', 'leaders', 'vacancies', 
            'documents', 'timetables', 'edu_infos', 'events', 'resources', 
            'culture_services', 'culture_arts', 'fine_arts'
        )