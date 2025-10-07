from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from .models import ImageModel, ImageSerializer
from . import serializers as S


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    lookup_field = 'id'
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_class(self):
        if self.action == 'list':
            return ImageSerializer
        if self.action == 'retrieve':
            return S.ImageDetailSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return S.ImageWriteSerializer
        return S.ImageDetailSerializer