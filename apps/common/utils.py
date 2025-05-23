from datetime import timezone
from django.core.files import File
from PIL import Image
from io import BytesIO
from django.utils import timezone, dateformat
import os

def split_file_name(filename):
    filename = filename.split(os.sep)[-1]
    return [''.join(filename.split('.')[:-1]), filename.split('.')[-1]]

def generate_upload_path(instance, filename):
    app_label = instance._meta.app_label
    model_name = instance._meta.model_name
    now = dateformat.format(timezone.now(), 'Y/m/d')
    file, exc = split_file_name(filename)

    filepath = '%s/%s/%s/%s.%s' % (
        app_label, model_name, now, file, exc
    )
    return filepath

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
