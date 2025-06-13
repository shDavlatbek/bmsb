from rest_framework import serializers
from apps.main.models import TimeTable


class TimeTableListSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    
    class Meta:
        model = TimeTable
        fields = [
            'id', 'title', 'file', 'school_name', 'created_at'
        ] 