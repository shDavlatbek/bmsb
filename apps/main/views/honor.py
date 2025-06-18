from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.common.mixins import IsActiveFilterMixin, SchoolScopedMixin
from apps.main.models import Honors
from apps.main.serializers.honor import HonorsListSerializer, HonorsDetailSerializer


class HonorsListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = Honors.objects.all()
    serializer_class = HonorsListSerializer
    school_field = "school"


class HonorsDetailView(IsActiveFilterMixin, SchoolScopedMixin, RetrieveAPIView):
    queryset = Honors.objects.all()
    serializer_class = HonorsDetailSerializer
    lookup_field = 'slug'
    school_field = "school" 