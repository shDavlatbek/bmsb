from typing import Dict
from apps.main.models import Menu
from rest_framework import serializers

class MenuSerializer(serializers.ModelSerializer):
    url      = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model  = Menu
        fields = ("title", "url", "children")   # add more fields if you need

    # resolves to get_absolute_url / "#" fallback we defined earlier
    def get_url(self, obj) -> str:
        return obj.get_absolute_url()

    # recurse ↓
    def get_children(self, obj) -> list[Dict[str, str], Dict[str, str]]:
        # .get_children() doesn’t hit the DB again if you prefetched (see view)
        qs = obj.get_children()
        if not qs:
            return []
        ser = MenuSerializer(qs, many=True, context=self.context)
        return ser.data