from rest_framework import serializers
from .models import Service, CultureService, CultureArt, FineArt, ServiceImage, CultureServiceFile


class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ['id', 'image', 'created_at']


class CultureServiceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CultureServiceFile
        fields = ['id', 'file', 'created_at']


class ServiceListSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id', 'name', 'slug', 'tags', 'image', 'created_at']

    def get_tags(self, obj):
        if obj.tags:
            return [tag.strip() for tag in obj.tags.split(',')]
        return []
    
    def get_image(self, obj):
        first_image = obj.service_images.first()
        if first_image and first_image.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(first_image.image.url)
            return first_image.image.url
        return None


class ServiceDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'slug', 'description', 'tags', 
            'images', 'created_at'
        ]
    
    def get_images(self, obj):
        request = self.context.get('request')
        images = []
        for service_image in obj.service_images.all():
            if service_image.image:
                if request:
                    images.append(request.build_absolute_uri(service_image.image.url))
                else:
                    images.append(service_image.image.url)
        return images
    
    def get_tags(self, obj):
        if obj.tags:
            return [tag.strip() for tag in obj.tags.split(',')]
        return []


class CultureServiceListSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = CultureService
        fields = ['id', 'name', 'slug', 'price', 'tags', 'image', 'created_at']

    def get_tags(self, obj):
        if obj.tags:
            return [tag.strip() for tag in obj.tags.split(',')]
        return []
    
    def get_image(self, obj):
        first_image = obj.service_images.first()
        if first_image and first_image.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(first_image.image.url)
            return first_image.image.url
        return None


class CultureServiceDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    service_files = CultureServiceFileSerializer(many=True, read_only=True)
    tags = serializers.SerializerMethodField()
    
    class Meta:
        model = CultureService
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'tags',
            'images', 'service_files', 'created_at'
        ]

    def get_images(self, obj):
        request = self.context.get('request')
        images = []
        for service_image in obj.service_images.all():
            if service_image.image:
                if request:
                    images.append(request.build_absolute_uri(service_image.image.url))
                else:
                    images.append(service_image.image.url)
        return images

    def get_tags(self, obj):
        if obj.tags:
            return [tag.strip() for tag in obj.tags.split(',')]
        return []


class CultureArtListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = CultureArt
        fields = [
            'id', 'name', 'slug', 
            'image', 'tags', 'created_at'
        ]

    def get_image(self, obj):
        first_image = obj.service_images.first()
        if first_image and first_image.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(first_image.image.url)
            return first_image.image.url
        return None
    
    def get_tags(self, obj):
        if obj.tags:
            return [tag.strip() for tag in obj.tags.split(',')]
        return []


class CultureArtDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    
    class Meta:
        model = CultureArt
        fields = [
            'id', 'name', 'slug', 'description', 'tags', 'email', 'phone_number',
            'author_image', 'author_name', 'author_musical_instrument', 
            'author_direction', 'author_honor', 'images', 'created_at'
        ]

    def get_images(self, obj):
        request = self.context.get('request')
        images = []
        for service_image in obj.service_images.all():
            if service_image.image:
                if request:
                    images.append(request.build_absolute_uri(service_image.image.url))
                else:
                    images.append(service_image.image.url)
        return images

    def get_tags(self, obj):
        if obj.tags:
            return [tag.strip() for tag in obj.tags.split(',')]
        return []


class FineArtListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = FineArt
        fields = [
            'id', 'name', 'slug', 
            'image', 'tags', 'created_at'
        ]

    def get_image(self, obj):
        first_image = obj.service_images.first()
        if first_image and first_image.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(first_image.image.url)
            return first_image.image.url
        return None
    
    def get_tags(self, obj):
        if obj.tags:
            return [tag.strip() for tag in obj.tags.split(',')]
        return []


class FineArtDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    
    class Meta:
        model = FineArt
        fields = [
            'id', 'name', 'slug', 'description', 'tags', 'email', 'phone_number',
            'author_image', 'author_name', 'author_musical_instrument', 
            'author_direction', 'author_honor', 'images', 'created_at'
        ]

    def get_images(self, obj):
        request = self.context.get('request')
        images = []
        for service_image in obj.service_images.all():
            if service_image.image:
                if request:
                    images.append(request.build_absolute_uri(service_image.image.url))
                else:
                    images.append(service_image.image.url)
        return images

    def get_tags(self, obj):
        if obj.tags:
            return [tag.strip() for tag in obj.tags.split(',')]
        return [] 