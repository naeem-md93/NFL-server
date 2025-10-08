import os
import uuid
from django.db import models
from rest_framework import serializers

from closet_image.models import ImageModel


class ItemModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    caption = models.CharField(max_length=255, blank=True)
    width = models.PositiveIntegerField(default=0, blank=True, null=True)
    height = models.PositiveIntegerField(default=0, blank=True, null=True)
    box_x = models.FloatField(blank=False, null=False, default=0)
    box_y = models.FloatField(blank=False, null=False, default=0)
    box_w = models.FloatField(blank=False, null=False, default=0)
    box_h = models.FloatField(blank=False, null=False, default=0)
    path = models.ImageField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    image = models.ForeignKey(ImageModel, on_delete=models.CASCADE, related_name="items", related_query_name="image", null=True, blank=True)

    class Meta:
        db_table = "closet_items"

    def __str__(self):
        return f"({self.id}) | {self.caption}"


class ItemListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = ItemModel
        fields = (
            "id", "source", "type", "caption", "width", 'height',
            "box_x", "box_y", "box_w", "box_h",
            "path", "url", "created_at", "updated_at"
        )
        
    def get_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return obj.url
        return request.build_absolute_uri(obj.url)