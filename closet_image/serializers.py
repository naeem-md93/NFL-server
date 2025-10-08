import os
from rest_framework import serializers

from closet_item.models import ItemListSerializer

from .models import ImageModel


SERVER_URL = os.getenv('SERVER_URL')

  
class ImageDetailSerializer(serializers.ModelSerializer):
    items = ItemListSerializer(many=True, read_only=True)
    file = serializers.ImageField(write_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = ImageModel
        fields = (
            "id", "source", "name", "width", "height", "path", "url", "created_at", "updated_at",
            "items",
            "file"
        )

    def get_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return obj.url
        return request.build_absolute_uri(obj.url)

