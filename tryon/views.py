import os
import uuid
import json
import base64
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


# from recommendation.models import RecommendationModel
# from recommendation.serializers import RecommendationDetailSerializer
#
# from .models import TryOnModel
# from .serializers import TryOnDetailSerializer




def post__get_tryon(photo_obj, outfit_id, mime_type):
    photo_path = os.path.join(settings.MEDIA_ROOT, photo_obj.photo_path.path)
    photo = open(photo_path, "rb")

    outfit = RecommendationModel.objects.get(pk=outfit_id)
    outfit = RecommendationDetailSerializer(outfit).data

    images = {
        "photo": photo,
    }

    for i, it in enumerate(outfit["items"]):
        images[f"item{i}"] = open("." + it["path"], "rb")

    res = requests.post(TRYON_URL, files=images).json()["result"]
    img_bytes = base64.b64decode(res)
    image_file = ContentFile(img_bytes, name=f"{photo_obj.id}.png")
    saved_name = default_storage.save(f"tryon/result/{photo_obj.id}.png", image_file)
    url = os.path.join(settings.MEDIA_URL, saved_name)

    photo_obj.result_url = url
    photo_obj.save()

    return photo_obj


def post__process_one_file(file, outfit_id):

    file_name = file.name
    mime_type = file.content_type

    _id = uuid.uuid4().hex
    ext = os.path.splitext(file_name)[1]
    save_name = f"{_id}{ext}"
    os.makedirs("./media/tryon/photo/", exist_ok=True)
    saved_name = default_storage.save(f"./tryon/photo/{save_name}", file)
    url = os.path.join(settings.MEDIA_URL, saved_name)

    photo = TryOnModel.objects.create(**{
        "id": _id,
        "photo_file_name": file_name,
        "photo_path": saved_name,
        "photo_url": url,
    })
    photo.save()

    photo_obj = post__get_tryon(photo, outfit_id, mime_type)

    return photo_obj


class TryOnView(APIView):
    def post(self, request):
        # i_serializer =
        try:
            photo = request.data.pop("photo")[0]
            outfit_id = request.data.pop("outfit_id")[0]

            photo_obj = post__process_one_file(photo, outfit_id)
            data = TryOnDetailSerializer(photo_obj).data

            return Response({"result": data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(repr(e))
            return Response([repr(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
