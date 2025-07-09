from rest_framework import generics
from django.db.models import Prefetch

from apps.common.mixins import IsActiveFilterMixin, SchoolScopedMixin
from ..models import Direction, DirectionSchool
from ..serializers.direction import DirectionListSerializer, DirectionDetailSerializer


class DirectionListView(IsActiveFilterMixin, SchoolScopedMixin, generics.ListAPIView):
    queryset = DirectionSchool.objects.all()
    serializer_class = DirectionListSerializer
    school_field = "school"


class DirectionDetailView(IsActiveFilterMixin, SchoolScopedMixin, generics.RetrieveAPIView):
    queryset = DirectionSchool.objects.select_related('direction').prefetch_related(
        'subjects',
        'musical_instruments'
    )
    serializer_class = DirectionDetailSerializer
    lookup_field = 'direction__slug'
    lookup_url_kwarg = 'slug'
    school_field = "school" 