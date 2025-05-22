from django.urls import path
from .views.menu import MenuView
from .views.school import CheckSchoolView, SchoolView
from .views.school_life import SchoolLifeView
from .views.banner import BannerListView

urlpatterns = [
    path('check-school', CheckSchoolView.as_view(), name='check-school'),
    path('menus', MenuView.as_view(), name='menu'),
    path('banners', BannerListView.as_view(), name='banner'),
    path('schools', SchoolView.as_view(), name='school'),
    path('school-lifes', SchoolLifeView.as_view(), name='school-life'),
]

