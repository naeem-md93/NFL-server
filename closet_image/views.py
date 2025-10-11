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
SERVER_URL = os.getenv("SERVER_URL")


def post__process_items(path, image_obj, items):
    img = Image.open(os.path.join(settings.MEDIA_ROOT, path)).convert("RGB")
    width, height = img.width, img.height
    
    for it in items:
        x, y, w, h = it["box_x"], it["box_y"], it["box_w"], it["box_h"]
        x0 = int(x * width)
        y0 = int(y * height)
        x1 = int((x + w) * width) + 1
        y1 = int((y + h) * height) + 1
        
        cropped_img = img.crop((x0, y0, x1, y1))
        
        _id = uuid.uuid4().hex
        save_path = os.path.join(f"closet/items/{_id}.png")
        os.makedirs("./media/closet/items/", exist_ok=True)

        cropped_img.save(os.path.join(settings.MEDIA_ROOT, save_path), "png")
        
        it["source"] = "MyCloset"
        it["image"] = image_obj
        it["width"] = width
        it["height"] = height
        it["path"] = save_path
        it['url'] = os.path.join("/media/", save_path)
        it = ItemModel.objects.create(**it)
        it.save()


def post__extract_items(path):
    img_path = os.path.join(settings.MEDIA_ROOT, path)
    img = open(img_path, "rb")

    resp = requests.post(
        f"{AI_URL}/api/ai/extract-items/",
        files={"file": img},
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
    os.makedirs("./media/closet/images/", exist_ok=True)
    saved_name = default_storage.save(f"./closet/images/{save_name}", file)
    url = os.path.join(settings.MEDIA_URL, saved_name)

    image = ImageModel.objects.create(**{
        "id": _id,
        "source": SOURCE,
        "name": file_name,
        "path": saved_name,
        "url": url,
        "width": width,
        "height": height,
    })    
    image.save()
    
    items = post__extract_items(saved_name)
    print(f"MMMMMDDDD {items}")
    
    post__process_items(saved_name, image, items)
    
    return image


class ImageView(APIView):
    def get(self, request):
        print(f'ImageView get: {request.GET.dict()}')
        try:
            _id = request.GET.dict().pop('id', None)
            if _id is None:
                sources = ImageModel.objects.all()
                serializer = ImageListSerializer(sources, many=True, context={"request": request})
            else:
                sources = ImageModel.objects.get(id=_id)
                serializer = ImageDetailSerializer(sources, context={"request": request})
            return Response(serializer.data)
        except Exception as e:
            print(repr(e))
            return Response([repr(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        print(f'ImageView post: {request.data}')
        print(f"file:", request.FILES)
        try:
            i_serializer = ImageDetailSerializer(data=request.data, context={"request": request})
            if i_serializer.is_valid():
                file = i_serializer.validated_data.pop("file")
                image = post__process_one_file(file)
                f_serializer = ImageDetailSerializer(image, context={"request": request})
                    
                return Response(f_serializer.data, status=status.HTTP_201_CREATED)
            return Response(i_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(repr(e))
            return Response([repr(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        print(f'ImageView delete: {request.data}')
        try:
            _id = request.data.pop('id')

            source = ImageModel.objects.get(id=_id)
            source.delete()

            return Response(data={"Deleted Successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(repr(e))
            return Response([repr(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
