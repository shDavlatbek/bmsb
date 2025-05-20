from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.common.mixins import IsActiveFilterMixin
from apps.main.models import SchoolLife
from apps.main.serializers.school_life import SchoolLifeSerializer


class SchoolLifeListView(IsActiveFilterMixin, ListAPIView):
    serializer_class = SchoolLifeSerializer
    queryset = SchoolLife.objects.all()
    permission_classes = []
    
    def get_queryset(self):
        queryset = super().get_queryset()
        school = self.request.school
        if school:
            queryset = queryset.filter(school=school)
        return queryset


class SchoolLifeDetailView(IsActiveFilterMixin, RetrieveAPIView):
    serializer_class = SchoolLifeSerializer
    queryset = SchoolLife.objects.all()
    permission_classes = []
    
    def get_queryset(self):
        queryset = super().get_queryset()
        school = self.request.school
        if school:
            queryset = queryset.filter(school=school)
        return queryset 