from django.urls import path
from apps.news.views import (
    NewsListView,
    NewsDetailView,
    CategoryListView,
)


urlpatterns = [
    path('', NewsListView.as_view(), name='news-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('<slug:slug>/', NewsDetailView.as_view(), name='news-detail'),
] 