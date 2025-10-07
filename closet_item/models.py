import os
import uuid
from django.db import models
from rest_framework import serializers

from closet_image.models import ImageModel


def item_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join('closet', "items", f"{instance.id}.{ext}")

class ItemModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=255, null=True, blank=True)
    caption = models.CharField(max_length=255, blank=True)
    brx = models.FloatField(blank=False, null=False, default=0)
    bry = models.FloatField(blank=False, null=False, default=0)
    brw = models.FloatField(blank=False, null=False, default=0)
    brh = models.FloatField(blank=False, null=False, default=0)
    bax = models.PositiveIntegerField(blank=False, null=False, default=0)
    bay = models.PositiveIntegerField(blank=False, null=False, default=0)
    baw = models.PositiveIntegerField(blank=False, null=False, default=0)
    bah = models.PositiveIntegerField(blank=False, null=False, default=0)
    url = models.ImageField(upload_to=item_upload_path, null=True, blank=True)
    image = models.ForeignKey(ImageModel, on_delete=models.CASCADE, related_name="items", related_query_name="image", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "closet_items"

    def __str__(self):
        return f"({self.id}) | {self.caption}"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemModel
        fields = (
            "id", "type", "caption",
            "brx", "bry", "brw", "brh",
            "bax", "bay", "baw", "bah",
            "url", "created_at"
        )