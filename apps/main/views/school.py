from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.common.mixins import IsActiveFilterMixin
from apps.main.models import School
from apps.main.serializers.school import SchoolSerializer


class CheckSchoolView(APIView):
    def get(self, request):
        return Response({'school': request.school.slug if request.school else None})


class SchoolListView(IsActiveFilterMixin, ListAPIView):
    serializer_class = SchoolSerializer
    queryset = School.objects.all()
    permission_classes = []


class SchoolDetailView(IsActiveFilterMixin, RetrieveAPIView):
    serializer_class = SchoolSerializer
    queryset = School.objects.all()
    permission_classes = []
    lookup_field = 'slug'