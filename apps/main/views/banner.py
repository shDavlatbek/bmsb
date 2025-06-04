from rest_framework.generics import ListAPIView
from apps.common.mixins import SchoolScopedMixin, IsActiveFilterMixin
from apps.main.models import Banner
from apps.main.serializers.banner import BannerSerializer


class BannerListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    serializer_class = BannerSerializer
    queryset = Banner.objects.all()
    permission_classes = []
    pagination_class = None