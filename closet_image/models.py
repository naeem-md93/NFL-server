import os
import uuid
from django.db import models
from django.conf import settings
from rest_framework import serializers
from closet_source.models import SourceModel


def image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join('closet', "images", f"{instance.id}.{ext}")


class ImageModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.ForeignKey(SourceModel, on_delete=models.CASCADE, related_name="images", related_query_name="source", null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    url = models.FilePathField(path=settings.MEDIA_ROOT, blank=True, null=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "closet_images"

    def __str__(self):
        return f"({self.id}) | {self.url.name}"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ("id", "name", "width", "height", "url", "created_at")
