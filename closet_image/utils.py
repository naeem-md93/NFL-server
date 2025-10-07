import copy
import io
from PIL import Image


def byte_to_pillow(image_bytes):
    img_copy = copy.deepcopy(image_bytes)
    raw = img_copy.read()
    image = Image.open(io.BytesIO(raw))
    return raw, image, image.width, image.height

