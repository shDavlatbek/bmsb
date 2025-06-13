from datetime import timezone
import hashlib
from uuid import uuid4
from django.core.files import File
from django.core.files.storage import default_storage
from PIL import Image
from io import BytesIO
from django.utils import timezone, dateformat
import os


def generate_upload_path(instance, filename: str) -> str:
    """
    <app>/<model>/<Y/m/d>/<filename>   (adds -<8-char-uuid> *only* if a clash)
    """
    app_label  = instance._meta.app_label
    model_name = instance._meta.model_name
    today      = dateformat.format(timezone.now(), "Y/m/d")

    name, ext  = os.path.splitext(filename)
    base_dir   = f"{app_label}/{model_name}/{today}"

    candidate  = f"{base_dir}/{name}{ext.lower()}"
    # If the exact name exists, keep trying until it's unique
    while default_storage.exists(candidate):
        candidate = f"{base_dir}/{name}-{uuid4().hex[:8]}{ext.lower()}"

    return candidate


def compress(image):
    if not image:
        return image
    if '.svg' in image.name:
        return image
    img = Image.open(image)
    img_size = len(img.fp.read())

    if img_size / (1024 * 1024) > 1:
        if image.name.split('.')[1] == 'png':
            img = img.convert('RGB', palette=Image.ADAPTIVE, colors=256)
            thumb_io = BytesIO()
            img.save(thumb_io, 'jpeg', quality=70, optimize=True)
            new_image = File(thumb_io, name=image.name.split('.')[0] + '.jpg')
        else:
            thumb_io = BytesIO()
            img.save(thumb_io, 'jpeg', quality=20, optimize=True)
            new_image = File(thumb_io, name=image.name)
        return new_image
    else:
        return image
