import os
from io import BytesIO
from django.core.files import File
from PIL import Image
from django.utils import timezone, dateformat
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler
from pathlib import Path
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _



def custom_exception_handler(exc, context):
    handlers = {
        "ValidationError": _handle_validation_error,
    }
    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](exc, context)
    return response


def _handle_validation_error(exc, context):
    response = exception_handler(exc, context)
    errors = as_serializer_error(exc)

    if response is not None:
        response.data = {"status_code": response.status_code, "errors": []}
        make_pretty_error(response.data, errors)
    return response


def make_pretty_error(data, errors):
    for error in errors:
        if isinstance(errors[error][0], ErrorDetail) and len(errors[error]) == 1:
            data["errors"].append({"error": f"{error}_{errors[error][0].code}", "message": errors[error][0]})
        elif isinstance(errors[error][0], dict) and len(errors[error]) >= 1:
            for er in errors[error]:
                make_pretty_error(data, er)
        else:
            data["errors"].append({"error": f"{error}", "message": errors[error]})


def compress(image):
    if not image:
        return image
    if '.svg' in image.name:
        return image
    img = Image.open(image)
    img_size = len(img.fp.read())

    if img_size / (1024 * 1024) > 1:
        if image.name.split(".")[1] == "png":
            img = img.convert("RGB", palette=Image.ADAPTIVE, colors=256)
            thumb_io = BytesIO()
            img.save(thumb_io, 'jpeg', quality=70, optimize=True)
            new_image = File(thumb_io, name=image.name.split(".")[0] + ".jpg")
        else:
            thumb_io = BytesIO()
            img.save(thumb_io, 'jpeg', quality=20, optimize=True)
            new_image = File(thumb_io, name=image.name)
        return new_image
    else:
        return image


def generate_upload_path(instance, filename):
    """"""
    app_label = instance._meta.app_label
    model_name = instance._meta.model_name
    now = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
    file, exc = split_file_name(filename)

    filepath = "%s/%s/%s-%s.%s" % (
        app_label, model_name, file, now, exc
    )
    return filepath


def split_file_name(filename):
    """path/file.exe => file, exe"""
    filename = filename.split(os.sep)[-1]
    return [''.join(filename.split('.')[:-1]), filename.split('.')[-1]]


def file_size(value):  # add this to some file where you can import it from
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')
