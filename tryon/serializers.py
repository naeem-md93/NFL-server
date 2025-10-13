import os
from rest_framework import serializers

from recommendation.serializers import RecommendationListSerializer

from .models import TryOnModel


class TryOnListSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    result_url = serializers.SerializerMethodField()

    class Meta:
        model = TryOnModel
        fields = (
            "id",
            "photo_name", "photo_path", "photo_mime_type", "result_path",
            "created_at", "updated_at",
        )

    def get_photo_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return obj.photo_path.url
        return request.build_absolute_uri(obj.photo_path.url)

    def get_result_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return obj.result_path.url
        return request.build_absolute_uri(obj.result_path.url)


class TryOnDetailSerializer(serializers.ModelSerializer):
    recommendation = RecommendationListSerializer(many=True, read_only=True)
    photo_url = serializers.SerializerMethodField()
    result_url = serializers.SerializerMethodField()

    class Meta:
        model = TryOnModel
        fields = (
            "id",
            "photo_name", "photo_path", "photo_mime_type", "result_path",
            "recommendation",
            "created_at", "updated_at",
        )

    def get_photo_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return obj.photo_path.url
        return request.build_absolute_uri(obj.photo_path.url)

    def get_result_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return obj.result_path.url
        return request.build_absolute_uri(obj.result_path.url)

