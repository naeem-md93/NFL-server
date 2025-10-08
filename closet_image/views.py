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

from closet_item.models import ItemModel

from . import utils
from .models import ImageModel, ImageListSerializer
from .serializers import ImageDetailSerializer


AI_URL= os.getenv("AI_URL")


def post__extract_items(file, width, height):
    resp = requests.post(
        f"{AI_URL}/api/ai/extract-items/",
        files={"file": file},
        data={"width": width, "height": height}
    )

    return resp.json()


def post__process_one_file(file):
    SOURCE = "MyCloset"
            
    file_name = file.name
    mime_type = file.content_type
    width, height = file.image.size
    
    _id = uuid.uuid4().hex
    ext = os.path.splitext(file_name)[1]
    save_name = f"{_id}{ext}"
    saved_name = default_storage.save(
        f"./closet/images/{save_name}",
        file
    )
    url = default_storage.url(save_name)
    print(f'{saved_name=}')
    print(f"{url=}")
    
    
    image = ImageModel.objects.create(**{
        "id": _id,
        "source": SOURCE,
        "name": file_name,
        "url": image_url,
        "width": width,
        "height": height,
    })    
    image.save()
    
    items = post__extract_items(file, width, height)
    for it in items:
        it["image"] = image
        it["width"] = width
        it["height"] = height
        it['source'] = SOURCE
        it = ItemModel(**it)
        it.save()    
    
    return image


class ImageView(APIView):
    def get(self, request):
        _id = request.GET.dict().pop('id', None)
        if _id is None:
            sources = ImageModel.objects.all()
            serializer = ImageListSerializer(sources, many=True)
        else:
            sources = ImageModel.objects.get(id=_id)
            serializer = ImageDetailSerializer(sources)
        return Response(serializer.data)

    def post(self, request):
        
        i_serializer = ImageDetailSerializer(data=request.data)
        if i_serializer.is_valid():
            file = i_serializer.validated_data.pop("file")
            print(vars(file))
            image = post__process_one_file(file)
            f_serializer = ImageDetailSerializer(image)
                
            return Response(f_serializer.data, status=status.HTTP_201_CREATED)
        return Response(i_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request):
    #     _id = request.data.pop('id')

    #     i_serializer = ImageDetailSerializer(data=request.data)
    #     if i_serializer.is_valid():
    #         validated_data = i_serializer.validated_data
            
    #         source = validated_data.pop("source", None)
    #         if source is not None:
    #             source = SourceModel.objects.get(name=source)
            
    #         items = validated_data.pop("items", None)
    #         if items is not None:
    #             validated_data["items"] = items
    #         source = ImageModel.objects.get(id=_id)
    #         for key, value in i_serializer.validated_data.items():
    #             setattr(source, key, value)
    #         source.save()
    #         f_serializer = ImageDetailSerializer(source)
    #         return Response(f_serializer.data, status=status.HTTP_200_OK)
    #     return Response(i_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def patch(self, request):
    #     _id = request.data.pop('id')

    #     i_serializer = ImageDetailSerializer(data=request.data)
    #     if i_serializer.is_valid():
    #         source = ImageModel.objects.get(id=_id)
    #         for key, value in i_serializer.validated_data.items():
    #             setattr(source, key, value)
    #         source.save()
    #         f_serializer = ImageDetailSerializer(source)
    #         return Response(f_serializer.data, status=status.HTTP_200_OK)
    #     return Response(i_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):

        _id = request.data.pop('id')

        source = ImageModel.objects.get(id=_id)
        source.delete()

        return Response(data={"Deleted Successfully"}, status=status.HTTP_200_OK)