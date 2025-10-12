import os
from rest_framework import serializers

from .models import ImageModel, ItemModel


# Id input
class ImageIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ("id", )


class ItemIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemModel
        fields = ("id", )



# List
class ImageListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = ImageModel
        fields = (
            "id",
            "source", "name", "width", "height", "mime_type",
            "url",
            "created_at", "updated_at"
        )

    def get_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return obj.path.url
        return request.build_absolute_uri(obj.path.url)


class ItemListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = ItemModel
        fields = (
            "id",
            "source", "type", "caption", "width", 'height',
            "box_x", "box_y", "box_w", "box_h",
            "url",
            "created_at", "updated_at"
        )

    def get_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return obj.path.url
        return request.build_absolute_uri(obj.path.url)


# Detail
class ImageDetailSerializer(serializers.ModelSerializer):
    items = ItemListSerializer(many=True, read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = ImageModel
        fields = (
            "id",
            "source", "name", "width", "height", "mime_type",
            "url",
            "created_at", "updated_at",
            "items",
        )

    def get_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return obj.path.url
        return request.build_absolute_uri(obj.path.url)


class ItemDetailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    image = ImageListSerializer(read_only=True)

    class Meta:
        model = ItemModel
        fields = (
            "id",
            "source", "type", "caption", "width", "height",
            "box_x", "box_y", "box_w", "box_h",
            "url",
            "created_at", "updated_at",
            "image",
        )

    def get_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return obj.url
        return request.build_absolute_uri(obj.url)


class ImageCreateSerializer(serializers.ModelSerializer):
    file = serializers.ImageField()
    class Meta:
        model = ImageModel
        fields = ("file", )


class ItemCreateSerializer(serializers.ModelSerializer):
    file = serializers.ImageField()

    class Meta:
        model = ItemModel
        fields = ("file", "type", "caption", "box_x", "box_y", "box_w", "box_h")