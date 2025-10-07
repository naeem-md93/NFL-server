import uuid
from django.db import models
from rest_framework import serializers


class SourceModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'closet_sources'


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceModel
        fields = ("id", "name", "created_at")
