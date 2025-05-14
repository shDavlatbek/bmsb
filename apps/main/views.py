from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import MenuItem
from rest_framework import serializers


class MenuItemSerializer(serializers.ModelSerializer):
    url      = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model  = MenuItem
        fields = ("id", "title", "url", "children")   # add more fields if you need

    # resolves to get_absolute_url / "#" fallback we defined earlier
    def get_url(self, obj) -> str:
        return obj.get_absolute_url()

    # recurse ↓
    def get_children(self, obj) -> list[dict]:
        # .get_children() doesn’t hit the DB again if you prefetched (see view)
        qs = obj.get_children()
        if not qs:
            return []
        ser = MenuItemSerializer(qs, many=True, context=self.context)
        return ser.data


class MenuView(ListAPIView):
    """
    GET /api/menu/ → returns the whole menu as a nested JSON tree
    """
    serializer_class = MenuItemSerializer
    pagination_class = None
    permission_classes = []         
    
    queryset = (
        MenuItem.objects.root_nodes()
        .prefetch_related(
            "children",
            "children__children",
            "children__children__children",
        )     # if you use LinkType.OBJECT
    )

