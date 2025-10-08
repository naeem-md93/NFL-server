import os
import uuid
from django.db import models
from django.conf import settings
from rest_framework import serializers


class ImageModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "closet_images"

    def __str__(self):
        return f"({self.id}) | {self.name}"


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ("id", "source", "name", "width", "height", "url", "created_at", "updated_at")