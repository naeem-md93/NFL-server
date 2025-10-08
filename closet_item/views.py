import os
import uuid
import copy
import json
import requests
from PIL import Image
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.core.files.storage import default_storage


from closet_item.models import ItemModel, ItemListSerializer
from .serializers import ItemDetailSerializer


AI_URL= os.getenv("AI_URL")
SERVER_URL = os.getenv("SERVER_URL")


class ItemView(APIView):
    def get(self, request):
        _id = request.GET.dict().pop('id', None)
        if _id is None:
            sources = ItemModel.objects.all()
            serializer = ItemListSerializer(sources, many=True, context={"request": request})
        else:
            sources = ItemModel.objects.get(id=_id)
            serializer = ItemDetailSerializer(sources, context={"request": request})
        print(serializer.data)
        return Response(serializer.data)
