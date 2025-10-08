import copy
import io
from PIL import Image


def byte_to_pillow(file_obj):
    
    try:
        pos = file_obj.tell()
    except (AttributeError, IOError):
        pos = None
        
    raw = file_obj.read()
    if pos is not None:
        try:
            file_obj.seek(pos)
        except Exception:
            # ignore if seek not supported
            pass

    image = Image.open(io.BytesIO(raw))
    # ensure image is loaded (some PIL lazy-load)
    image.load()
    
    return image, image.width, image.height

