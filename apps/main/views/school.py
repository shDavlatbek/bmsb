from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from apps.common.mixins import IsActiveFilterMixin
from apps.main.serializers.school import SchoolSerializer


class CheckSchoolView(APIView):
    def get(self, request):
        return Response({'school': request.school.slug if request.school else None})


class SchoolView(IsActiveFilterMixin, RetrieveAPIView):
    serializer_class = SchoolSerializer
    permission_classes = []
    filter_backends = []
    
    def get(self, request):
        if not request.school and not request.subdomain:
            return Response({'detail': None})
        
        serializer = SchoolSerializer(request.school)
        return Response(serializer.data)