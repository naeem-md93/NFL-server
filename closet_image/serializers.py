from rest_framework import serializers

from closet_item.models import ItemListSerializer

from .models import ImageModel

  
class ImageDetailSerializer(serializers.ModelSerializer):
    items = ItemListSerializer(many=True, read_only=True)
    file = serializers.ImageField(write_only=True)

    class Meta:
        model = ImageModel
        fields = (
            "id", "source", "name", "width", "height", "url", "created_at", "updated_at",
            "items",
            "file"
        )