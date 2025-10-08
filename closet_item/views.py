from rest_framework import viewsets

from .models import ItemModel, ItemListSerializer
from . import serializers as S


class ItemViewSet(viewsets.ModelViewSet):
    queryset = ItemModel.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'list':
            return ItemListSerializer
        if self.action == 'retrieve':
            return S.ItemDetailSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return S.ItemWriteSerializer
        return S.ItemDetailSerializer