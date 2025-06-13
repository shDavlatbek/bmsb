from rest_framework.generics import ListAPIView
from apps.common.mixins import IsActiveFilterMixin, SchoolScopedMixin
from apps.main.models import TimeTable
from apps.main.serializers.timetable import TimeTableListSerializer


class TimeTableListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = TimeTable.objects.all()
    serializer_class = TimeTableListSerializer
    school_field = "school"
    pagination_class = None 