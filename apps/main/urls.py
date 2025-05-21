from django.urls import path
from .views.menu import MenuView
from .views.school import CheckSchoolView, SchoolListView, SchoolDetailView
from .views.school_life import SchoolLifeListView, SchoolLifeDetailView
from .views.banner import BannerListView

urlpatterns = [
    path('menu/', MenuView.as_view(), name='menu'),
    path('banner/', BannerListView.as_view(), name='banner'),
    path('check-school/', CheckSchoolView.as_view(), name='check-school'),
    path('schools/', SchoolListView.as_view(), name='school-list'),
    path('schools/<slug:slug>/', SchoolDetailView.as_view(), name='school-detail'),
    path('school-life/', SchoolLifeListView.as_view(), name='school-life-list'),
    path('school-life/<int:pk>/', SchoolLifeDetailView.as_view(), name='school-life-detail'),
]

