from django.urls import path
from .views import (
    ServiceListView, ServiceDetailView,
    CultureServiceListView, CultureServiceDetailView,
    CultureArtListView, CultureArtDetailView,
    FineArtListView, FineArtDetailView
)

urlpatterns = [
    # Services
    # path('services/', ServiceListView.as_view(), name='service-list'),
    # path('services/<slug:slug>/', ServiceDetailView.as_view(), name='service-detail'),
    
    # Culture Services 
    path('culture-services/', CultureServiceListView.as_view(), name='culture-service-list'),
    path('culture-services/<slug:slug>/', CultureServiceDetailView.as_view(), name='culture-service-detail'),
    
    # Culture Art
    path('culture-arts/', CultureArtListView.as_view(), name='culture-art-list'),
    path('culture-arts/<slug:slug>/', CultureArtDetailView.as_view(), name='culture-art-detail'),
    
    # Fine Art
    path('fine-arts/', FineArtListView.as_view(), name='fine-art-list'),
    path('fine-arts/<slug:slug>/', FineArtDetailView.as_view(), name='fine-art-detail'),
] 