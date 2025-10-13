import uuid
from django.db import models

from recommendation.models import RecommendationModel


def tryon_photo_upload_path(instance, filename):
    """
    Generates the storage path: public/closet/images/<uuid>/<original_filename>
    The 'public' part is relative to your MEDIA_ROOT setting.
    """
    # Use the instance's UUID
    ext = filename.split('.')[-1]
    return f"tryon/photo/{instance.id}.{ext}"


def tryon_result_upload_path(instance, filename):
    """
    Generates the storage path: public/closet/images/<uuid>/<original_filename>
    The 'public' part is relative to your MEDIA_ROOT setting.
    """
    # Use the instance's UUID
    ext = filename.split('.')[-1]
    return f"tryon/result/{instance.id}.{ext}"


class TryOnModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo_name = models.CharField(max_length=255, null=True, blank=True)
    photo_path = models.ImageField(upload_to=tryon_photo_upload_path, null=True, blank=True)
    photo_mime_type = models.CharField(max_length=255, null=True, blank=True)
    result_path = models.ImageField(upload_to=tryon_result_upload_path, null=True, blank=True)
    recommendation = models.ForeignKey(RecommendationModel, on_delete=models.CASCADE, related_name="tryon", related_query_name="recommendation", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "tryons"

    def __str__(self):
        return f"({self.id})"