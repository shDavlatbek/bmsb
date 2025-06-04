from rest_framework import serializers
from ..models import Teacher, Direction, TeacherExperience


class DirectionBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ['id', 'name', 'slug']


class TeacherExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherExperience
        fields = ['id', 'title', 'start_date', 'end_date']


class TeacherListSerializer(serializers.ModelSerializer):
    direction = serializers.SerializerMethodField()
    
    class Meta:
        model = Teacher
        fields = ['id', 'full_name', 'slug', 'image', 'experience_years', 'direction', 'created_at']
    
    def get_direction(self, obj):
        first_direction = obj.directions.first()
        if first_direction:
            return first_direction.name
        return None


class TeacherDetailSerializer(serializers.ModelSerializer):
    directions = DirectionBasicSerializer(many=True, read_only=True)
    experiences = TeacherExperienceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Teacher
        fields = [
            'id', 'full_name', 'slug', 'image', 'experience_years',
            'directions', 'experiences', 'created_at'
        ] 