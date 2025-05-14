from modeltranslation.translator import translator, TranslationOptions
from .models import School


class SchoolTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'short_description', 'address')
    required_languages = ('uz',)


translator.register(School, SchoolTranslationOptions)