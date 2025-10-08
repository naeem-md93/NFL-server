import os
from rest_framework import serializers

from closet_image.models import ImageListSerializer

from .models import ItemModel


class ItemDetailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    image = ImageListSerializer(read_only=True)

    class Meta:
        model = ItemModel
        fields = (
            "id", "source", "type", "caption", "width", "height",
            "box_x", "box_y", "box_w", "box_h",
            "path", "url", "created_at", "updated_at"
            "image",
        )
        
    def get_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return obj.url
        return request.build_absolute_uri(obj.url)