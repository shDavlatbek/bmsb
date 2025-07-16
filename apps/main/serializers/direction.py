from rest_framework import serializers
from ..models import (
    DirectionSchool, Subject, MusicalInstrument, Teacher, 
    DirectionImage, DirectionVideo
)


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'slug', 'description', 'background_image', 'icon', 'created_at']


class MusicalInstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicalInstrument
        fields = ['id', 'name', 'slug', 'description', 'background_image', 'icon', 'created_at']


class TeacherBasicSerializer(serializers.ModelSerializer):
    direction = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    
    class Meta:
        model = Teacher
        fields = ['id', 'full_name', 'slug', 'image', 'experience_years', 'direction', 'subject']
    
    def get_direction(self, obj):
        first_direction = obj.directions.first()
        if first_direction:
            return first_direction.name
        return None

    def get_subject(self, obj):
        if obj.subject:
            return obj.subject.name
        return None
    

class DirectionListSerializer(serializers.ModelSerializer):
    # Direction fields accessed through the direction relationship
    name = serializers.CharField(source='direction.name', read_only=True)
    slug = serializers.CharField(source='direction.slug', read_only=True)
    icon = serializers.ImageField(source='direction.icon', read_only=True)
    background_image = serializers.ImageField(source='direction.background_image', read_only=True)
    
    class Meta:
        model = DirectionSchool
        fields = ['id', 'name', 'slug', 'icon', 'background_image', 'direction_image', 'founded_year', 'student_count', 'teacher_count', 'created_at']


class DirectionDetailSerializer(serializers.ModelSerializer):
    # Direction fields accessed through the direction relationship
    name = serializers.CharField(source='direction.name', read_only=True)
    slug = serializers.CharField(source='direction.slug', read_only=True)
    icon = serializers.ImageField(source='direction.icon', read_only=True)
    background_image = serializers.ImageField(source='direction.background_image', read_only=True)
    
    # DirectionSchool relationships
    subjects = SubjectSerializer(many=True, read_only=True)
    musical_instruments = MusicalInstrumentSerializer(many=True, read_only=True)
    gallery_images = serializers.SerializerMethodField()
    gallery_videos = serializers.SerializerMethodField()

    # Teachers that belong to this direction and school
    teachers = serializers.SerializerMethodField()
    
    class Meta:
        model = DirectionSchool
        fields = [
            'id', 'name', 'slug', 'description', 'icon', 'background_image', 'direction_image', 'founded_year', 
            'student_count', 'teacher_count', 'subjects', 
            'musical_instruments', 'teachers', 'gallery_images', 'gallery_videos', 'created_at'
        ]
    
    def get_gallery_images(self, obj):
        if obj.direction_images.exists():
            request = self.context.get('request')
            return [request.build_absolute_uri(img.image.url) for img in obj.direction_images.all() if img.image]
        return []

    def get_gallery_videos(self, obj):
        return [vid.video for vid in obj.direction_videos.all()]
    
    def get_teachers(self, obj):
        """Get teachers that belong to this direction and the same school"""
        if obj.school:
            # Get teachers from the same school that teach this direction
            teachers = Teacher.objects.filter(
                school=obj.school,
                directions=obj.direction,
                is_active=True
            )
            return TeacherBasicSerializer(teachers, many=True).data
        return [] 