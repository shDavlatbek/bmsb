from rest_framework.generics import ListAPIView
from apps.common.mixins import IsActiveFilterMixin, SchoolScopedMixin
from apps.main.models import FAQ
from apps.main.serializers.faq import FAQListSerializer


class FAQListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQListSerializer
    school_field = "school" 
    pagination_class = None