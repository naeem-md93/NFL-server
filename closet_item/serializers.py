from django.db import transaction
from rest_framework import serializers

from closet_image.models import ImageModel, ImageSerializer

from .models import ItemModel, ItemSerializer


class ItemDetailSerializer(serializers.ModelSerializer):
    image = ImageSerializer(read_only=True)

    class Meta:
        model = ItemModel
        fields = (
            "id", "type", "caption",
            "brx", "bry", "brw", "brh",
            "bax", "bay", "baw", "bah",
            "url",
            "image",
            "created_at"
        )


class ItemWriteSerializer(serializers.ModelSerializer):
    image_id = serializers.PrimaryKeyRelatedField(
        source="image",
        queryset=ImageModel.objects.all(),
        write_only=True
    )

    image = ImageSerializer(read_only=True)

    class Meta:
        model = ItemModel
        fields = (
            "id", "type", "caption",
            "brx", "bry", "brw", "brh",
            "bax", "bay", "baw", "bah",
            "url",
            "image_id", "image",
            "created_at"
        )
        read_only_fields = ['id', 'created_at']


    @transaction.atomic
    def create(self, validated_data):
        item = ItemModel.objects.create(**validated_data)
        return item

    @transaction.atomic
    def update(self, instance, validated_data):
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance