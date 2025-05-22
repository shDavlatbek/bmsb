
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _




def file_size(value):
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Fayl 5 MB dan katta bo\'lishi mumkin emas.')