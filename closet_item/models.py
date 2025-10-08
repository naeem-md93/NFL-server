import os
import uuid
from django.db import models
from rest_framework import serializers

from closet_image.models import ImageModel


class ItemModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=255, null=True, blank=True)
    caption = models.CharField(max_length=255, blank=True)
    width = models.PositiveIntegerField(default=0, blank=True, null=True)
    height = models.PositiveIntegerField(default=0, blank=True, null=True)
    box_x = models.FloatField(blank=False, null=False, default=0)
    box_y = models.FloatField(blank=False, null=False, default=0)
    box_w = models.FloatField(blank=False, null=False, default=0)
    box_h = models.FloatField(blank=False, null=False, default=0)
    url = models.ImageField(upload_to="closet/items/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    image = models.ForeignKey(ImageModel, on_delete=models.CASCADE, related_name="items", related_query_name="image", null=True, blank=True)

    class Meta:
        db_table = "closet_items"

    def __str__(self):
        return f"({self.id}) | {self.caption}"


class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemModel
        fields = (
            "id", "type", "caption", "width", 'height',
            "box_x", "box_y", "box_w", "box_h",
            "url", "created_at", "updated_at"
        )