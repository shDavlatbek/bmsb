from rest_framework.generics import ListAPIView
from apps.common.mixins import IsActiveFilterMixin, SchoolScopedMixin
from apps.main.models import SchoolLife
from apps.main.serializers.school_life import SchoolLifeSerializer


class SchoolLifeView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    serializer_class = SchoolLifeSerializer
    queryset = SchoolLife.objects.all()
    page_size = 3