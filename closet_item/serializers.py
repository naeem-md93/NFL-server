from rest_framework import serializers

from closet_image.models import ImageListSerializer

from .models import ItemModel


class ItemDetailSerializer(serializers.ModelSerializer):
    image = ImageListSerializer(read_only=True)

    class Meta:
        model = ItemModel
        fields = (
            "id", "type", "caption", "width", "height",
            "box_x", "box_y", "box_w", "box_h",
            "url", "created_at", "updated_at"
            "image",
        )