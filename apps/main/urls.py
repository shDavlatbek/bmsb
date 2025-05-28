from django.urls import path
from .views.menu import MenuView
from .views.school import SchoolView
from .views.school_life import SchoolLifeView
from .views.banner import BannerListView
from .views.direction import DirectionListView, DirectionDetailView
from .views.teacher import TeacherListView, TeacherDetailView

urlpatterns = [
    path('menus/', MenuView.as_view(), name='menu'),
    path('banners/', BannerListView.as_view(), name='banner'),
    path('school/', SchoolView.as_view(), name='school'),
    path('school-lifes/', SchoolLifeView.as_view(), name='school-life'),
    
    # Direction endpoints
    path('directions/', DirectionListView.as_view(), name='direction-list'),
    path('directions/<slug:slug>/', DirectionDetailView.as_view(), name='direction-detail'),
    
    # Teacher endpoints
    path('teachers/', TeacherListView.as_view(), name='teacher-list'),
    path('teachers/<slug:slug>/', TeacherDetailView.as_view(), name='teacher-detail'),
]

