from rest_framework import serializers
from ..models import EmailSubscription


class EmailSubscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSubscription
        fields = ['email']
        # Note: No school field - it's automatically assigned by SchoolScopedMixin 