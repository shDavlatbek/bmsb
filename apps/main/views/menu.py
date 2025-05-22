from rest_framework.generics import ListAPIView
from apps.common.mixins import SchoolScopedMixin, IsActiveFilterMixin
from apps.main.models import Menu
from apps.main.serializers.menu import MenuSerializer


class MenuView(IsActiveFilterMixin, SchoolScopedMixin, ListAPIView):
    serializer_class = MenuSerializer
    pagination_class = None
    permission_classes = []         
    filter_backends = []
    
    queryset = (
        Menu.objects.root_nodes()
        .prefetch_related(
            "children",
            "children__children",
            "children__children__children",
        )
    )