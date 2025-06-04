from rest_framework import generics

from apps.common.mixins import IsActiveFilterMixin, SchoolScopedMixin
from ..models import Teacher
from ..serializers.teacher import TeacherListSerializer, TeacherDetailSerializer


class TeacherListView(IsActiveFilterMixin, SchoolScopedMixin, generics.ListAPIView):
    queryset = Teacher.objects.all().prefetch_related('directions')
    serializer_class = TeacherListSerializer
    school_field = "school"


class TeacherDetailView(IsActiveFilterMixin, SchoolScopedMixin, generics.RetrieveAPIView):
    queryset = Teacher.objects.all().prefetch_related(
        'directions',
        'experiences'
    )
    serializer_class = TeacherDetailSerializer
    lookup_field = 'slug'
    school_field = "school" 