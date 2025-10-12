import os
import uuid
import json
import base64
import requests
from PIL import Image
from io import BytesIO

from django.core.files.base import ContentFile

from . import utils
from .models import ImageModel, ItemModel


def store_items(image_obj, items):
    img = Image.open(image_obj.path.path).convert("RGB")
    width, height = img.width, img.height

    item_objs = []
    for it in items:
        x, y, w, h = it.pop("bbox")
        x0 = int(x * width)
        y0 = int(y * height)
        x1 = int((x + w) * width) + 1
        y1 = int((y + h) * height) + 1

        cropped_img = img.crop((x0, y0, x1, y1))
        buffer = BytesIO()
        cropped_img.save(buffer, format="PNG")

        _id = uuid.uuid4().hex

        it_obj = ItemModel.objects.create(**{
            "id": _id,
            "source": "MyCloset",
            "type": it.pop("type"),
            "caption": it.pop("description"),
            "width": width,
            "height": height,
            "box_x": x,
            "box_y": y,
            "box_w": w,
            "box_h": h,
            "path": ContentFile(buffer.getvalue(), name=_id + ".png"),
        })
        it_obj.save()
        item_objs.append(it_obj)

    image_obj.items.set(item_objs)

def extract_items(image_obj):

    data_uri = utils.get_image_data_uri(image_obj.path.path, image_obj.mime_type)

    result = utils.get_response(
        utils.SYSTEM_PROMPT,
        utils.USER_PROMPT.format(
            caption_text="",
            image_metadata={"image_width": image_obj.width, "image_height": image_obj.height}
        ),
        data_uri
    )

    return result

def process_and_store_image(file):

    width, height = file.image.size
    image_obj = ImageModel.objects.create(**{
        "source": "MyCloset",
        "name": file.name,
        "width": width,
        "height": height,
        "mime_type": file.content_type,
        "path": file
    })
    image_obj.save()

    items = extract_items(image_obj)

    store_items(image_obj, items)

    return image_obj
