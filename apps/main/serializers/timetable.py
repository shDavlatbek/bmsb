from rest_framework import serializers
from apps.main.models import TimeTable


class TimeTableListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = [
            'id', 'title', 'file', 'created_at'
        ] 