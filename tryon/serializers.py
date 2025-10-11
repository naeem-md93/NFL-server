import os
from rest_framework import serializers

from recommendation.models import RecommendationListSerializer
from .models import TryOnModel


class TryOnDetailSerializer(serializers.ModelSerializer):
    recommendation = RecommendationListSerializer(many=True, read_only=True)
    photo_url = serializers.SerializerMethodField()
    result_url = serializers.SerializerMethodField()

    class Meta:
        model = TryOnModel
        fields = (
            "id",
            "photo_file_name", "photo_path", "photo_url", "result_url",
            "recommendation",
            "created_at", "updated_at",
        )

    def get_photo_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return obj.photo_url
        return request.build_absolute_uri(obj.photo_url)

    def get_result_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return obj.result_url
        return request.build_absolute_uri(obj.result_url)