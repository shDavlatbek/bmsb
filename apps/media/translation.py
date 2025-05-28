from modeltranslation.translator import translator, TranslationOptions
from .models import MediaCollection, MediaVideo


class MediaCollectionTranslationOptions(TranslationOptions):
    fields = ('title',)
    required_languages = ('uz',)

class MediaVideoTranslationOptions(TranslationOptions):
    fields = ('title',)
    required_languages = ('uz',)


translator.register(MediaCollection, MediaCollectionTranslationOptions)
translator.register(MediaVideo, MediaVideoTranslationOptions)