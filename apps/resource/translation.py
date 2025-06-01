from modeltranslation.translator import translator, TranslationOptions
from .models import ResourceVideo, ResourceFile


class ResourceVideoTranslationOptions(TranslationOptions):
    fields = ('title',)
    required_languages = ('uz',)


class ResourceFileTranslationOptions(TranslationOptions):
    fields = ('title',)
    required_languages = ('uz',)


translator.register(ResourceVideo, ResourceVideoTranslationOptions)
translator.register(ResourceFile, ResourceFileTranslationOptions) 