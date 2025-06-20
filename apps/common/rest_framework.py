import os
from io import BytesIO
from django.core.files import File
from PIL import Image
from django.utils import timezone, dateformat
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler
from rest_framework.pagination import PageNumberPagination
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


class Pagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 999
