from modeltranslation.translator import TranslationOptions, register
from . import models


@register(models.News)
class NewsTranslationOptions(TranslationOptions):
    fields = ("title", "content")