import os
import uuid
from django.db import models
from rest_framework import serializers

from closet.models import ItemModel


class RecommendationModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    compatibility = models.FloatField(default=0, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    items = models.ManyToManyField(ItemModel, related_name="recommendations")

    class Meta:
        db_table = "recommendations"

    def __str__(self):
        return f"({self.id}) | {self.description}"


class RecommendationListSerializer(serializers.Serializer):
    class Meta:
        model = RecommendationModel
        fields = ("id", "compatibility", "description", "created_at", "updated_at")