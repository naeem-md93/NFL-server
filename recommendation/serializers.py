import os
from rest_framework import serializers

from closet_item.models import ItemListSerializer

from .models import RecommendationModel


class RecommendationDetailSerializer(serializers.ModelSerializer):
    items = ItemListSerializer(many=True, read_only=True)
    
    class Meta:
        model = RecommendationModel
        fields = (
            "id", "compatibility", "description", "created_at", "updated_at",
            "items",
        )