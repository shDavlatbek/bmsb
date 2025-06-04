from modeltranslation.translator import translator, TranslationOptions
from .models import School, Menu, Banner, SchoolLife, Direction, Subject, MusicalInstrument, TeacherExperience, FAQ, Vacancy, Document, DocumentCategory, Staff, Leader


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


class FAQTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
    required_languages = ('uz',)


class VacancyTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'requirements', 'location')
    required_languages = ('uz',)


class DocumentCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = ('uz',)


class DocumentTranslationOptions(TranslationOptions):
    fields = ('title',)
    required_languages = ('uz',)


class StaffTranslationOptions(TranslationOptions):
    fields = ('full_name', 'position')
    required_languages = ('uz',)


class LeaderTranslationOptions(TranslationOptions):
    fields = ('full_name', 'position', 'description', 'working_days')
    required_languages = ('uz',)


translator.register(School, SchoolTranslationOptions)
translator.register(Menu, MenuTranslationOptions)
translator.register(Banner, BannerTranslationOptions)
translator.register(SchoolLife, SchoolLifeTranslationOptions)
translator.register(Direction, DirectionTranslationOptions)
translator.register(Subject, SubjectTranslationOptions)
translator.register(MusicalInstrument, MusicalInstrumentTranslationOptions)
translator.register(TeacherExperience, TeacherExperienceTranslationOptions)
translator.register(FAQ, FAQTranslationOptions)
translator.register(Vacancy, VacancyTranslationOptions)
translator.register(DocumentCategory, DocumentCategoryTranslationOptions)
translator.register(Document, DocumentTranslationOptions)
translator.register(Staff, StaffTranslationOptions)
translator.register(Leader, LeaderTranslationOptions)