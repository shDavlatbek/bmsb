from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.common.mixins import SchoolScopedMixin
from ..models import EmailSubscription
from ..serializers.email_subscription import EmailSubscriptionCreateSerializer


class EmailSubscriptionCreateView(SchoolScopedMixin, CreateAPIView):
    queryset = EmailSubscription.objects.all()
    serializer_class = EmailSubscriptionCreateSerializer
    school_field = "school"
    
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        
        # Check if email already exists for this school
        if EmailSubscription.objects.filter(school=request.school, email=email).exists():
            return Response(
                {'message': 'Bu email allaqachon obuna bo\'lgan.'},
                status=status.HTTP_200_OK
            )
        
        # Create new subscription
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(
            {'message': 'Email muvaffaqiyatli obuna bo\'ldi.'},
            status=status.HTTP_201_CREATED
        ) 