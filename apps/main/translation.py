from modeltranslation.translator import translator, TranslationOptions
from .models import School, Menu, Banner, SchoolLife, Direction, Subject, MusicalInstrument, TeacherExperience


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


class DirectionTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
    required_languages = ('uz',)


class SubjectTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
    required_languages = ('uz',)


class MusicalInstrumentTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
    required_languages = ('uz',)


class TeacherExperienceTranslationOptions(TranslationOptions):
    fields = ('title',)
    required_languages = ('uz',)


translator.register(School, SchoolTranslationOptions)
translator.register(Menu, MenuTranslationOptions)
translator.register(Banner, BannerTranslationOptions)
translator.register(SchoolLife, SchoolLifeTranslationOptions)
translator.register(Direction, DirectionTranslationOptions)
translator.register(Subject, SubjectTranslationOptions)
translator.register(MusicalInstrument, MusicalInstrumentTranslationOptions)
translator.register(TeacherExperience, TeacherExperienceTranslationOptions)