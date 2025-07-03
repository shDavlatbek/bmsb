from rest_framework import generics, status
from rest_framework.response import Response
from apps.common.mixins import SchoolScopedMixin
from ..models import ContactForm
from ..serializers.contact_form import ContactFormCreateSerializer


class ContactFormCreateView(SchoolScopedMixin, generics.CreateAPIView):
    """Create contact form requests - no authentication required"""
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormCreateSerializer
    school_field = "school"
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            "message": "So'rov muvaffaqiyatli yuborildi",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED) 