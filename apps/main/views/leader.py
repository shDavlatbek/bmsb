from rest_framework import generics

from apps.common.mixins import IsActiveFilterMixin, SchoolScopedMixin
from ..models import Leader
from ..serializers.leader import LeaderListSerializer, LeaderDetailSerializer


class LeaderListView(IsActiveFilterMixin, SchoolScopedMixin, generics.ListAPIView):
    queryset = Leader.objects.all()
    serializer_class = LeaderListSerializer
    school_field = "school"


class LeaderDetailView(IsActiveFilterMixin, SchoolScopedMixin, generics.RetrieveAPIView):
    queryset = Leader.objects.all()
    serializer_class = LeaderDetailSerializer
    lookup_field = 'slug'
    school_field = "school" 