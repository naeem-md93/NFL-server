from rest_framework import serializers

from closet_image.models import ImageSerializer
from .models import SourceModel, SourceSerializer

class SourceDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = SourceModel
        fields = (
            "id", "name",
            "images",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at")
