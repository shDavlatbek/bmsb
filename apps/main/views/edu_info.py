from rest_framework.generics import ListAPIView
from apps.common.mixins import IsActiveFilterMixin, SchoolScopedMixin
from ..models import EduInfo
from ..serializers.edu_info import EduInfoSerializer


class EduInfoListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = EduInfo.objects.all()
    serializer_class = EduInfoSerializer
    school_field = "school"
    pagination_class = None 