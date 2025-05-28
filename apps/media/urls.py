from django.urls import path
from . import views

app_name = 'media'

urlpatterns = [
    # Media collections endpoints
    path('collections/', views.MediaCollectionListView.as_view(), name='collection-list'),
    path('collections/<slug:slug>/', views.MediaCollectionDetailView.as_view(), name='collection-detail'),
    
    # Media images endpoint
    path('images/', views.MediaImageListView.as_view(), name='image-list'),
    
    # Media videos endpoint
    path('videos/', views.MediaVideoListView.as_view(), name='video-list'),
] 