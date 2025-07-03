from rest_framework import generics
from apps.common.mixins import IsActiveFilterMixin, SchoolScopedMixin
from ..models import Comments
from ..serializers.comments import CommentsListSerializer, CommentsDetailSerializer


class CommentsListView(IsActiveFilterMixin, SchoolScopedMixin, generics.ListAPIView):
    """List all comments for the current school"""
    queryset = Comments.objects.all()
    serializer_class = CommentsListSerializer
    school_field = "school"


class CommentsDetailView(IsActiveFilterMixin, SchoolScopedMixin, generics.RetrieveAPIView):
    """Get a specific comment by ID"""
    queryset = Comments.objects.all()
    serializer_class = CommentsDetailSerializer
    lookup_field = 'id'
    school_field = "school" 