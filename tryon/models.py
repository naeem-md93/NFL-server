import os
import uuid
from django.db import models
from rest_framework import serializers


from recommendation.models import RecommendationModel


class TryOnModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo_file_name = models.CharField(max_length=255, null=True, blank=True)
    photo_path = models.ImageField(null=True, blank=True)
    photo_url = models.URLField(null=True, blank=True)
    result_url = models.URLField(null=True, blank=True)
    recommendation = models.ForeignKey(RecommendationModel, on_delete=models.CASCADE, related_name="tryon", related_query_name="recommendation", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "tryons"

    def __str__(self):
        return f"({self.id})"


class TryOnListSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    result_url = serializers.SerializerMethodField()

    class Meta:
        model = TryOnModel
        fields = (
            "id",
            "photo_file_name", "photo_path", "photo_url", "result_url",
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