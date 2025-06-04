from rest_framework import serializers
from apps.main.models import Vacancy


class VacancyListSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Vacancy
        fields = [
            'id', 'title', 'slug', 'description', 'salary', 'requirements',
            'location', 'type', 'type_display', 'school_name', 'created_at'
        ] 