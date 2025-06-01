from rest_framework.generics import ListAPIView
from apps.common.mixins import IsActiveFilterMixin, SchoolScopedMixin
from apps.main.models import Vacancy
from apps.main.serializers.vacancy import VacancyListSerializer


class VacancyListView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer
    school_field = "school" 