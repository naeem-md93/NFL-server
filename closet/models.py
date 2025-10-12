import uuid
from PIL import Image
from django.db import models


def image_upload_path(instance, filename):
    """
    Generates the storage path: public/closet/images/<uuid>/<original_filename>
    The 'public' part is relative to your MEDIA_ROOT setting.
    """
    # Use the instance's UUID
    ext = filename.split('.')[-1]
    return f"closet/images/{instance.id}.{ext}"


class ImageModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    mime_type = models.CharField(max_length=255, null=True, blank=True)
    path = models.ImageField(upload_to=image_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "closet_images"

    def __str__(self):
        return f"({self.id}) | {self.name}"


def item_upload_path(instance, filename):
    """
    Generates the storage path: public/closet/images/<uuid>/<original_filename>
    The 'public' part is relative to your MEDIA_ROOT setting.
    """
    # Use the instance's UUID
    ext = filename.split('.')[-1]
    return f"closet/items/{instance.id}.{ext}"


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
    path = models.ImageField(upload_to=item_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    image = models.ForeignKey(
        ImageModel,
        on_delete=models.CASCADE,
        related_name="items",
        related_query_name="image",
        null=True,
        blank=True
    )

    class Meta:
        db_table = "closet_items"

    def __str__(self):
        return f"({self.id}) | {self.caption}"