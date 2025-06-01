from datetime import timezone
import hashlib
from django.core.files import File
from PIL import Image
from io import BytesIO
from django.utils import timezone, dateformat
import os


def generate_upload_path(instance, filename: str) -> str:
    """
    <app>/<model>/<Y/m/d>/<filename>
    """
    app_label  = instance._meta.app_label
    model_name = instance._meta.model_name
    today      = dateformat.format(timezone.now(), "Y/m/d")

    name, ext  = os.path.splitext(filename)

    return (
        f"{app_label}/{model_name}/{today}/"
        f"{name}{ext.lower()}"
    )

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
