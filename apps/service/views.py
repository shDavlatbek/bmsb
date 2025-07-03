from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.common.mixins import IsActiveFilterMixin, SchoolScopedMixin
from .models import Service, CultureService, CultureArt, FineArt
from .serializers import (
    ServiceListSerializer, ServiceDetailSerializer,
    CultureServiceListSerializer, CultureServiceDetailSerializer,
    CultureArtListSerializer, CultureArtDetailSerializer,
    FineArtListSerializer, FineArtDetailSerializer
)

# Create your views here.

class ServiceListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceListSerializer
    school_field = "school"


class ServiceDetailView(IsActiveFilterMixin, SchoolScopedMixin, RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceDetailSerializer
    lookup_field = 'slug'
    school_field = "school"


class CultureServiceListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = CultureService.objects.all()
    serializer_class = CultureServiceListSerializer
    school_field = "school"


class CultureServiceDetailView(IsActiveFilterMixin, SchoolScopedMixin, RetrieveAPIView):
    queryset = CultureService.objects.all()
    serializer_class = CultureServiceDetailSerializer
    lookup_field = 'slug'
    school_field = "school"


class CultureArtListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = CultureArt.objects.all()
    serializer_class = CultureArtListSerializer
    school_field = "school"


class CultureArtDetailView(IsActiveFilterMixin, SchoolScopedMixin, RetrieveAPIView):
    queryset = CultureArt.objects.all()
    serializer_class = CultureArtDetailSerializer
    lookup_field = 'slug'
    school_field = "school"


class FineArtListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = FineArt.objects.all()
    serializer_class = FineArtListSerializer
    school_field = "school"


class FineArtDetailView(IsActiveFilterMixin, SchoolScopedMixin, RetrieveAPIView):
    queryset = FineArt.objects.all()
    serializer_class = FineArtDetailSerializer
    lookup_field = 'slug'
    school_field = "school"
