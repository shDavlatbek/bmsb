from modeltranslation.translator import translator, TranslationOptions
from .models import School, Menu, Banner, SchoolLife


class MenuTranslationOptions(TranslationOptions):
    fields = ('title',)
    required_languages = ('uz',)

class SchoolTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'short_description', 'address')
    required_languages = ('uz',)

class BannerTranslationOptions(TranslationOptions):
    fields = ('title', 'button_text')
    required_languages = ('uz',)


class SchoolLifeTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
    required_languages = ('uz',)


translator.register(School, SchoolTranslationOptions)
translator.register(Menu, MenuTranslationOptions)
translator.register(Banner, BannerTranslationOptions)
translator.register(SchoolLife, SchoolLifeTranslationOptions)