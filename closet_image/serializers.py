import os
import copy
import uuid
from PIL import Image
from django.core.files.storage import default_storage
from django.db import transaction
from rest_framework import serializers

from closet_source.models import SourceModel, SourceSerializer
from closet_item.models import ItemModel, ItemSerializer
from core import settings

from . import utils
from .models import ImageModel, ImageSerializer


AI_URL = os.getenv('AI_URL')
SAVE_DIR = os.path.join(settings.MEDIA_ROOT, "closet", 'images')
os.makedirs(SAVE_DIR, exist_ok=True)

    
class ImageDetailSerializer(serializers.ModelSerializer):
    source = SourceSerializer(read_only=True)
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = ImageModel
        fields = (
            "id", "name", "width", "height", "url",
            "source",
            "items",
            "created_at"
        )


class ImageWriteSerializer(serializers.ModelSerializer):
    item_ids = serializers.PrimaryKeyRelatedField(
        source="items",
        queryset=ItemModel.objects.all(),
        many=True,
        write_only=True,
        required=False
    )
    items = ItemSerializer(read_only=True, many=True)
    files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = ImageModel
        fields = (
            "id", "name", "width", "height", "url",
            "source", "item_ids", "items",
            "created_at",
            "files"
        )
        read_only_fields = ['id', 'created_at']


    @transaction.atomic
    def create(self, validated_data):

        files = validated_data.pop('files', [])
        source = validated_data.pop('source', "MyCloset")

        source, _ = SourceModel.objects.get_or_create(name=source)

        created = []
        for f in files:
            name = copy.deepcopy(f.name)

            _id = uuid.uuid4().hex
            ext = os.path.splitext(f.name)[1]
            filename = f"{_id}{ext}"
            relative_path = os.path.join("closet", "images", filename)

            # Save uploaded file into Django storage
            # default_storage.save accepts a File or ContentFile
            saved_name = default_storage.save(relative_path, f)
            saved_path = default_storage.path(saved_name)  # absolute filesystem path (only for FileSystemStorage)

            # If you need to read image dimensions, open saved file with PIL
            # (opening the file from storage avoids touching the original UploadedFile)
            with default_storage.open(saved_name, 'rb') as opened:
                img = Image.open(opened)
                width, height = img.size
                img.close()

            image = ImageModel.objects.create(**{
                "id": _id,
                "source": source,
                "name": name,
                "url": saved_name,  # string stored by FileField, e.g. "closet/images/<uuid>.jpg"
                "width": width,
                "height": height,
            })
            created.append(image)

        return created

    @transaction.atomic
    def update(self, instance, validated_data):
        items = validated_data.pop("items", None)

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        if items is not None:
            instance.items.set(items)

        return instance






#
# class AddImagesView(APIView):
#     """
#     POST /api/closet/images/add-images/  (multipart/form-data with files)
#     field expected: 'files' (multiple). This view attempts several fallbacks.
#     """
#     parser_classes = APIView.parser_classes  # keeps default; DRF handles multipart
#
#     def post(self, request):
#         files = request.FILES.getlist('files')
#         if not files:
#             return Response({'detail': 'No files provided'}, status=status.HTTP_400_BAD_REQUEST)
#
#         created = []
#         for f in files:
#             ff = copy.deepcopy(f)
#             fff = copy.deepcopy(f)
#
#             _, _, width, height = utils.byte_to_pillow(ff)
#             ci = ClosetImage.objects.create(image=f, name=f.name, width=width, height=height)
#             resp = requests.post(f"{AI_URL}/api/ai/extract-items/", files={'file': fff})
#             resp = resp.json()
#             for r in resp:
#                 r["closet_image"] = ci
#
#             ClosetItem.objects.bulk_create([ClosetItem(**r) for r in resp])
#             created.append(ci)
#
#         serializer = ClosetImagesSerializer(created, many=True, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#