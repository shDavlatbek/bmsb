from django.urls import path
from .views import (
    ResourceVideoListView, 
    ResourceVideoDetailView,
    ResourceFileListView, 
    ResourceFileDetailView
)

urlpatterns = [
    # Resource Video endpoints
    path('videos/', ResourceVideoListView.as_view(), name='resource-video-list'),
    # path('videos/<int:pk>/', ResourceVideoDetailView.as_view(), name='resource-video-detail'),
    
    # Resource File endpoints
    path('files/', ResourceFileListView.as_view(), name='resource-file-list'),
    # path('files/<int:pk>/', ResourceFileDetailView.as_view(), name='resource-file-detail'),
] 