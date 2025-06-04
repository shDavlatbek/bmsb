from rest_framework import generics

from apps.common.mixins import IsActiveFilterMixin, SchoolScopedMixin
from ..models import Staff
from ..serializers.staff import StaffListSerializer


class StaffListView(IsActiveFilterMixin, SchoolScopedMixin, generics.ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffListSerializer
    school_field = "school" 