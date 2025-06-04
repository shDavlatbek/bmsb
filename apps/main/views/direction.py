from rest_framework import generics
from django.db.models import Prefetch

from apps.common.mixins import IsActiveFilterMixin
from ..models import Direction, DirectionSchool
from ..serializers.direction import DirectionListSerializer, DirectionDetailSerializer


class DirectionListView(IsActiveFilterMixin, generics.ListAPIView):
    queryset = Direction.objects.all()
    serializer_class = DirectionListSerializer
    
    def get_queryset(self):
        # Get directions that belong to the current school through DirectionSchool
        # Get the current school from request
        if hasattr(self.request, 'school') and self.request.school:
            # Find DirectionSchool for current school and get its directions
            direction_school = DirectionSchool.objects.filter(
                school=self.request.school,
                is_active=True
            ).first()
            
            if direction_school:
                direction_ids = direction_school.directions.values_list('id', flat=True)
                qs = Direction.objects.filter(id__in=direction_ids)
                # Apply IsActiveFilterMixin filtering
                return self.apply_active_filter(qs)
            else:
                return Direction.objects.none()
        
        # If no school context, return empty queryset
        return Direction.objects.none()
    
    def apply_active_filter(self, qs):
        """Apply the active filter logic from IsActiveFilterMixin"""
        if not hasattr(qs.model, 'is_active'):
            return qs
            
        show_inactive = self.request.query_params.get('show_inactive', 'false').lower() == 'true'
        
        if show_inactive and self.request.user.is_staff:
            return qs
        else:
            return qs.filter(is_active=True)


class DirectionDetailView(IsActiveFilterMixin, generics.RetrieveAPIView):
    queryset = Direction.objects.all()
    serializer_class = DirectionDetailSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        # Prefetch related data for better performance
        qs = Direction.objects.prefetch_related(
            'subjects',
            'musical_instruments',
            'teachers'
        )
        
        # Get the current school from request
        if hasattr(self.request, 'school') and self.request.school:
            # Find DirectionSchool for current school and get its directions
            direction_school = DirectionSchool.objects.filter(
                school=self.request.school,
                is_active=True
            ).first()
            
            if direction_school:
                direction_ids = direction_school.directions.values_list('id', flat=True)
                qs = qs.filter(id__in=direction_ids)
                # Apply IsActiveFilterMixin filtering
                return self.apply_active_filter(qs)
            else:
                return qs.none()
        
        # If no school context, return empty queryset
        return qs.none()
    
    def apply_active_filter(self, qs):
        """Apply the active filter logic from IsActiveFilterMixin"""
        if not hasattr(qs.model, 'is_active'):
            return qs
            
        show_inactive = self.request.query_params.get('show_inactive', 'false').lower() == 'true'
        
        if show_inactive and self.request.user.is_staff:
            return qs
        else:
            return qs.filter(is_active=True) 