import os
from rest_framework import serializers

from closet.serializers import ItemListSerializer, ItemIdSerializer

from .models import RecommendationModel


class RecommendationListSerializer(serializers.Serializer):
    class Meta:
        model = RecommendationModel
        fields = (
            "id",
            "compatibility", "description",
            "created_at", "updated_at"
        )


class RecommendationDetailSerializer(serializers.ModelSerializer):
    items = ItemListSerializer(many=True, read_only=True)
    
    class Meta:
        model = RecommendationModel
        fields = (
            "id",
            "compatibility", "description",
            "created_at", "updated_at",
            "items",
        )


class RecommendationCreateSerializer(serializers.ModelSerializer):
    query = serializers.CharField(allow_blank=True, allow_null=True)
    occasions = serializers.ListSerializer(child=serializers.CharField(allow_null=True, allow_blank=True), allow_null=True, allow_empty=True)
    items = serializers.ListSerializer(child=serializers.CharField(allow_null=True, allow_blank=True), allow_null=True, allow_empty=True)

    class Meta:
        model = RecommendationModel
        fields = ("query", "occasions", "items")