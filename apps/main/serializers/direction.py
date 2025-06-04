from rest_framework import serializers
from ..models import Direction, Subject, MusicalInstrument, Teacher


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'slug', 'description', 'image']


class MusicalInstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicalInstrument
        fields = ['id', 'name', 'slug', 'description', 'image']


class TeacherBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'full_name', 'slug', 'image', 'experience_years']


class DirectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ['id', 'name', 'slug', 'icon', 'image', 'founded_year', 'student_count', 'teacher_count', 'created_at']


class DirectionDetailSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    musical_instruments = MusicalInstrumentSerializer(many=True, read_only=True)
    teachers = TeacherBasicSerializer(many=True, read_only=True)
    
    class Meta:
        model = Direction
        fields = [
            'id', 'name', 'slug', 'description', 'icon', 'image', 'founded_year', 
            'student_count', 'teacher_count', 'subjects', 
            'musical_instruments', 'teachers', 'created_at'
        ] 