from modeltranslation.translator import translator, TranslationOptions
from .models import CultureService, CultureArt, FineArt, Service


class ServiceTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'tags')
    required_languages = ('uz',)


class CultureServiceTranslationOptions(TranslationOptions):
    fields = ()
    required_languages = ('uz',)


class CultureArtTranslationOptions(TranslationOptions):
    fields = ('author_name', 'author_musical_instrument', 'author_direction', 'author_honor')
    required_languages = ('uz',)


class FineArtTranslationOptions(TranslationOptions):
    fields = ('author_name', 'author_musical_instrument', 'author_direction', 'author_honor')
    required_languages = ('uz',)


translator.register(Service, ServiceTranslationOptions)
translator.register(CultureService, CultureServiceTranslationOptions)
translator.register(CultureArt, CultureArtTranslationOptions)
translator.register(FineArt, FineArtTranslationOptions) 